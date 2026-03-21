#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Lolibrary.org 商品图片抓取脚本 - SQLite 版本（优化版）

特性：
- 使用 UUID 生成 64 位长整数作为主键
- 支持增量抓取/全量抓取
- 支持断点续传（每页保存状态）
- 自动下载图片到本地磁盘
- SQLite WAL 模式优化并发写入
- 图片下载不使用延迟（仅页面请求使用延迟）
- 完善的事务保护和异常处理
"""

import sys
import io

# 强制使用 UTF-8 编码输出（解决 Windows 控制台编码问题）
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

import requests
import json
import re
import time
import sqlite3
import os
import uuid
from urllib.parse import urljoin, urlparse
from datetime import datetime, timezone
from pathlib import Path
from bs4 import BeautifulSoup
from typing import List, Dict, Optional, Tuple, Any


def uuid_to_long() -> int:
    """将 UUID 转换为 64 位长整数"""
    uid = uuid.uuid4()
    uid_bytes = uid.bytes
    high = int.from_bytes(uid_bytes[:8], byteorder='big', signed=False)
    low = int.from_bytes(uid_bytes[8:], byteorder='big', signed=False)
    return (high ^ low) & 0x7FFFFFFFFFFFFFFF


class LolibraryScraper:
    """Lolibrary.org 商品抓取器"""
    
    BASE_URL = "https://lolibrary.org"
    
    def __init__(self, delay: float = 1.0, state_file: Optional[str] = None, 
                 db_path: Optional[str] = None,
                 image_dir: str = r"C:\Users\Administrator\Pictures\lolibrary"):
        """初始化抓取器"""
        self.delay = delay
        self.state_file = Path(state_file) if state_file else Path(__file__).parent.parent / "output" / "scraper_state.json"
        self.db_path = db_path
        self.image_dir = Path(image_dir)
        self.last_scrape_time: Optional[datetime] = None
        self.current_page: int = 1
        self.total_items_scraped: int = 0
        self.db_conn: Optional[sqlite3.Connection] = None
        
        # 确保图片目录存在
        self.image_dir.mkdir(parents=True, exist_ok=True)
        
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        self.skipped_count = 0
        self.downloaded_images = 0
        self.items_in_page = 0  # 当前页已处理商品数（用于频繁保存状态）
        
        # 加载状态
        self._load_state()
        
        # 连接数据库
        if db_path:
            self._init_db()
    
    def _init_db(self) -> None:
        """初始化数据库（优化版）"""
        try:
            # 使用 WAL 模式和优化参数
            self.db_conn = sqlite3.connect(self.db_path, timeout=30, isolation_level=None)
            self.db_conn.execute("PRAGMA journal_mode=WAL")
            self.db_conn.execute("PRAGMA synchronous=NORMAL")
            self.db_conn.execute("PRAGMA cache_size=10000")
            self.db_conn.execute("PRAGMA foreign_keys=ON")
            self.db_conn.execute("PRAGMA temp_store=MEMORY")
            
            cursor = self.db_conn.cursor()
            
            # 创建商品表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS lolibrary_items (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    url TEXT NOT NULL UNIQUE,
                    brand TEXT,
                    category TEXT,
                    published_at DATETIME,
                    scraped_at DATETIME,
                    extra_info TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # 创建图片表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS lolibrary_images (
                    id INTEGER PRIMARY KEY,
                    item_id INTEGER NOT NULL,
                    image_url TEXT NOT NULL UNIQUE,
                    local_path TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (item_id) REFERENCES lolibrary_items(id) ON DELETE CASCADE
                )
            ''')
            
            # 创建索引
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_items_name ON lolibrary_items(name)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_items_brand ON lolibrary_items(brand)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_items_category ON lolibrary_items(category)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_items_published ON lolibrary_items(published_at)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_items_url ON lolibrary_items(url)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_images_item_id ON lolibrary_images(item_id)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_images_url ON lolibrary_images(image_url)')
            
            self.db_conn.commit()
            print(f"[OK] 数据库已连接：{self.db_path} (WAL 模式优化)")
        except Exception as e:
            print(f"[ERROR] 数据库初始化失败：{e}")
            self.db_conn = None
    
    def _load_state(self) -> None:
        """加载状态"""
        if self.state_file.exists():
            try:
                with open(self.state_file, 'r', encoding='utf-8') as f:
                    state = json.load(f)
                    last_time_str = state.get('last_scrape_time')
                    if last_time_str:
                        self.last_scrape_time = datetime.fromisoformat(last_time_str)
                    # 增量爬取时总是从第 1 页开始（最新商品），直到追上已抓取商品
                    # 全量爬取时从上次页码继续
                    is_incremental = self.last_scrape_time is not None
                    if is_incremental:
                        self.current_page = 1
                        print(f"[OK] 增量爬取模式 - 从第 1 页开始，直到追上已抓取商品")
                    else:
                        self.current_page = state.get('current_page', 1)
                        print(f"[OK] 全量爬取模式 - 从第 {self.current_page} 页继续")
                    self.total_items_scraped = state.get('total_items_scraped', 0)
            except Exception as e:
                print(f"[WARN] 加载状态失败：{e}，将从第 1 页开始")
                self.current_page = 1
    
    def _save_state(self) -> None:
        """保存状态（原子写入）"""
        try:
            self.state_file.parent.mkdir(parents=True, exist_ok=True)
            state = {
                'last_scrape_time': datetime.now(timezone.utc).isoformat(),
                'last_run': datetime.now().isoformat(),
                'current_page': self.current_page,
                'total_items_scraped': self.total_items_scraped
            }
            # 原子写入：先写临时文件再重命名
            temp_file = self.state_file.with_suffix('.tmp')
            with open(temp_file, 'w', encoding='utf-8') as f:
                json.dump(state, f, indent=2)
            temp_file.replace(self.state_file)
        except Exception as e:
            print(f"[ERROR] 保存状态失败：{e}")
    
    def _save_state_if_needed(self) -> None:
        """每处理 10 个商品保存一次状态（防止中断丢失进度）"""
        self.items_in_page += 1
        if self.items_in_page % 10 == 0:
            self._save_state()
    
    def _get_soup(self, url: str, max_retries: int = 3) -> Optional[BeautifulSoup]:
        """获取页面，带重试机制"""
        for attempt in range(max_retries):
            try:
                time.sleep(self.delay)
                response = self.session.get(url, timeout=30)
                response.raise_for_status()
                return BeautifulSoup(response.text, 'html.parser')
            except requests.exceptions.Timeout as e:
                print(f"[WARN] 获取页面超时 {url} (尝试 {attempt + 1}/{max_retries}): {e}")
                if attempt < max_retries - 1:
                    print("  等待 30 秒后重试...")
                    time.sleep(30)
            except requests.exceptions.RequestException as e:
                print(f"[ERROR] 获取页面失败 {url} (尝试 {attempt + 1}/{max_retries}): {e}")
                if attempt < max_retries - 1:
                    print("  等待 30 秒后重试...")
                    time.sleep(30)
                else:
                    return None
            except Exception as e:
                print(f"[ERROR] 未知错误 {url}: {e}")
                return None
        return None
    
    def _download_image(self, image_url: str, image_id: int, max_retries: int = 3) -> Optional[str]:
        """下载图片，带重试机制（不使用延迟）"""
        try:
            parsed = urlparse(image_url)
            ext = parsed.path.split('.')[-1] if '.' in parsed.path else 'jpg'
            if ext not in ['jpg', 'jpeg', 'png', 'gif', 'webp']:
                ext = 'jpg'
            
            local_filename = f"{image_id}.{ext}"
            local_path = self.image_dir / local_filename
            
            # 如果文件已存在，跳过下载
            if local_path.exists():
                return str(local_path)
            
            for attempt in range(max_retries):
                try:
                    response = self.session.get(image_url, timeout=30)
                    response.raise_for_status()
                    
                    with open(local_path, 'wb') as f:
                        f.write(response.content)
                    
                    self.downloaded_images += 1
                    return str(local_path)
                except requests.exceptions.Timeout as e:
                    print(f"[WARN] 下载图片超时 (尝试 {attempt + 1}/{max_retries}): {e}")
                    if attempt < max_retries - 1:
                        time.sleep(5)
                except requests.exceptions.RequestException as e:
                    print(f"[ERROR] 下载图片失败 (尝试 {attempt + 1}/{max_retries}): {e}")
                    if attempt < max_retries - 1:
                        time.sleep(5)
                    else:
                        return None
                except Exception as e:
                    print(f"[ERROR] 下载图片未知错误：{e}")
                    return None
            return None
        except Exception as e:
            print(f"[ERROR] 下载图片异常：{e}")
            return None
    
    def get_item_urls_from_page(self, page_num: int) -> List[str]:
        """获取指定页的商品 URL 列表"""
        url = f"{self.BASE_URL}/search?sort=added_new&page={page_num}"
        soup = self._get_soup(url)
        if not soup:
            return []
        
        items = []
        
        # 查找所有 /items/ 开头的链接
        for link in soup.find_all('a', href=re.compile(r'/items/[^/]+$')):
            href = link.get('href')
            if href:
                full_url = urljoin(self.BASE_URL, href)
                if full_url not in items:
                    items.append(full_url)
        
        return items
    
    def extract_item_data(self, item_url: str) -> Optional[Dict]:
        """提取商品数据"""
        try:
            soup = self._get_soup(item_url)
            if not soup:
                return None
            
            # 提取名称
            name = None
            h1 = soup.find('h1')
            if h1:
                name = h1.get_text(strip=True)
            if not name:
                print(f"[WARN] 无法提取商品名称：{item_url}")
                return None
            
            # 提取发布时间
            published_time = None
            time_elem = soup.find('time')
            if time_elem:
                datetime_attr = time_elem.get('datetime')
                if datetime_attr:
                    try:
                        published_time = datetime.fromisoformat(datetime_attr.replace('Z', '+00:00'))
                    except Exception as e:
                        print(f"[WARN] 解析时间失败：{e}")
            
            # 增量模式下，不再仅通过时间判断跳过
            # 而是通过数据库 URL 去重，确保不会漏掉全量期间新上架的商品
            # （这些商品可能发布时间早于 last_scrape_time，但实际是新的）
            if published_time and self.last_scrape_time:
                if published_time <= self.last_scrape_time:
                    # 标记为"可能已抓取"，但仍返回数据让 save_item_to_db 通过 URL 判断
                    pass  # 不跳过，继续处理
            
            # 提取品牌
            brand = None
            brand_heading = soup.find('h4', string='Brand')
            if brand_heading:
                brand_link = brand_heading.find_next('a')
                if brand_link:
                    brand = brand_link.get_text(strip=True)
            
            # 提取类目
            category = None
            category_heading = soup.find('h4', string='Category')
            if category_heading:
                category_link = category_heading.find_next('a')
                if category_link:
                    category = category_link.get_text(strip=True).replace(',', '').strip()
            
            # 提取额外信息
            extra_info = {}
            for h4 in soup.find_all('h4'):
                field_name = h4.get_text(strip=True)
                if field_name in ['Item Info', 'Images']:
                    continue
                
                value = None
                next_elem = h4.find_next_sibling()
                if next_elem:
                    if next_elem.name == 'a':
                        value = next_elem.get_text(strip=True)
                    elif next_elem.name == 'p':
                        value = next_elem.get_text(strip=True)
                    elif next_elem.name:
                        links = next_elem.find_all('a')
                        if links:
                            values = [link.get_text(strip=True).replace(',', '').strip() for link in links]
                            value = values if len(values) > 1 else values[0] if values else None
                        else:
                            value = next_elem.get_text(strip=True)
                
                if value:
                    extra_info[field_name.replace('?', '').strip()] = value
            
            # 提取图片 URL
            image_urls = []
            images_heading = soup.find('h4', string='Images')
            if images_heading:
                parent = images_heading.parent
                if parent:
                    for link in parent.find_all('a', href=re.compile(r'https://lolibrary\.global\.ssl\.fastly\.net/images/')):
                        img_url = link.get('href')
                        if img_url and img_url not in image_urls:
                            image_urls.append(img_url)
            
            return {
                'name': name,
                'url': item_url,
                'brand': brand,
                'category': category,
                'published_at': published_time.isoformat() if published_time else None,
                'scraped_at': datetime.now(timezone.utc).isoformat(),
                'extra_info': extra_info,
                'image_urls': image_urls
            }
        except Exception as e:
            print(f"[ERROR] 提取商品数据失败 {item_url}: {e}")
            return None
    
    def save_item_to_db(self, item: Dict, is_full_scrape: bool = False) -> bool:
        """
        保存商品到数据库（带事务保护）
        
        Args:
            item: 商品数据
            is_full_scrape: 是否全量模式（全量模式下重复不报错）
        """
        if not self.db_conn:
            return False
        
        try:
            cursor = self.db_conn.cursor()
            
            # 检查商品是否已存在
            cursor.execute('SELECT id FROM lolibrary_items WHERE url = ?', (item['url'],))
            if cursor.fetchone():
                # 已存在，全量模式下这是正常的
                if is_full_scrape:
                    print(f"  [SKIP] 已存在：{item['name'][:40]}...")
                return False
            
            # 生成 UUID 长整数 ID
            item_id = uuid_to_long()
            
            # 开启事务
            cursor.execute('BEGIN IMMEDIATE')
            
            try:
                # 插入商品
                extra_info_json = json.dumps(item.get('extra_info', {}), ensure_ascii=False) if item.get('extra_info') else None
                cursor.execute('''
                    INSERT INTO lolibrary_items (id, name, url, brand, category, published_at, scraped_at, extra_info)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    item_id, item['name'], item['url'], item.get('brand'), item.get('category'),
                    item.get('published_at'), item['scraped_at'], extra_info_json
                ))
                
                # 插入图片（先下载，再一起提交）
                image_ids = []
                local_paths = []
                for img_url in item.get('image_urls', []):
                    # 检查图片是否已存在
                    cursor.execute('SELECT id FROM lolibrary_images WHERE image_url = ?', (img_url,))
                    if cursor.fetchone():
                        continue
                    
                    image_id = uuid_to_long()
                    local_path = self._download_image(img_url, image_id)
                    
                    image_ids.append(image_id)
                    local_paths.append(local_path)
                
                # 批量插入图片记录
                for img_url, img_id, local_path in zip(item['image_urls'], image_ids, local_paths):
                    cursor.execute('''
                        INSERT INTO lolibrary_images (id, item_id, image_url, local_path)
                        VALUES (?, ?, ?, ?)
                    ''', (img_id, item_id, img_url, local_path))
                
                # 提交事务
                self.db_conn.commit()
                return True
                
            except Exception as e:
                # 回滚事务
                self.db_conn.rollback()
                print(f"[ERROR] 保存商品到数据库失败：{e}")
                return False
                
        except Exception as e:
            print(f"[ERROR] 数据库操作异常：{e}")
            return False
    
    def scrape(self, max_items: Optional[int] = None) -> int:
        """抓取商品"""
        print(f"\n[{datetime.now()}] 开始抓取...")
        print(f"从第 {self.current_page} 页开始")
        print(f"延迟：{self.delay}秒/请求")
        is_full_scrape = self.last_scrape_time is None
        print(f"模式：{'全量' if is_full_scrape else '增量'}\n")
        
        total_new = 0
        consecutive_no_data = 0
        consecutive_skipped = 0
        is_incremental = not is_full_scrape
        
        try:
            while True:
                if max_items and total_new >= max_items:
                    print(f"\n[OK] 已达到最大数量：{max_items}")
                    break
                
                print(f"\n[PAGE {self.current_page}] 获取中...")
                urls = self.get_item_urls_from_page(self.current_page)
                
                if not urls:
                    consecutive_no_data += 1
                    if consecutive_no_data >= 3:
                        print("[INFO] 连续 3 页无数据，停止")
                        break
                    print(f"[WARN] 第{self.current_page}页无数据，进入下一页")
                    self.current_page += 1
                    self._save_state()
                    continue
                
                consecutive_no_data = 0
                print(f"  找到 {len(urls)} 个商品")
                
                new_on_page = 0
                skipped_on_page = 0
                self.items_in_page = 0
                is_full_scrape = self.last_scrape_time is None
                
                for i, url in enumerate(urls, 1):
                    if max_items and total_new >= max_items:
                        break
                    
                    data = self.extract_item_data(url)
                    if data:
                        if self.save_item_to_db(data, is_full_scrape=is_full_scrape):
                            total_new += 1
                            new_on_page += 1
                            self.total_items_scraped += 1
                            print(f"  [{i}/{len(urls)}] OK - {data['name'][:40]}... ({len(data['image_urls'])}张图片)")
                        else:
                            # 全量模式下重复不算连续跳过
                            skipped_on_page += 1
                            if not is_full_scrape:
                                consecutive_skipped += 1
                    else:
                        skipped_on_page += 1
                    
                    # 每 10 个商品保存一次状态
                    self._save_state_if_needed()
                
                print(f"  本页新增：{new_on_page}, 跳过：{skipped_on_page}, 总计：{total_new}")
                
                # 保存状态
                self._save_state()
                
                # 如果连续跳过太多，可能已经抓完了（仅增量模式）
                # 阈值设为 100，确保多爬几页直到确认都是已爬过的商品
                if is_incremental and consecutive_skipped >= 100:
                    print("[INFO] 连续跳过 100 个商品，已抓取完毕（含全量期间新上架商品）")
                    break
                
                # 进入下一页
                self.current_page += 1
        
        except KeyboardInterrupt:
            print("\n[WARN] 用户中断，保存状态...")
            self._save_state()
        except Exception as e:
            print(f"\n[ERROR] 抓取异常：{e}")
            import traceback
            traceback.print_exc()
            self._save_state()
        
        print(f"\n{'='*50}")
        print(f"完成！新增：{total_new} 个商品，下载：{self.downloaded_images} 张图片")
        print(f"跳过：{self.skipped_count} 个商品（增量模式）")
        print(f"最终页码：{self.current_page}")
        print(f"{'='*50}")
        return total_new
    
    def finish(self):
        """关闭数据库连接"""
        if self.db_conn:
            try:
                self.db_conn.close()
                print("[OK] 数据库连接已关闭")
            except Exception as e:
                print(f"[ERROR] 关闭数据库失败：{e}")


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Lolibrary.org 商品图片抓取工具')
    parser.add_argument('--max-items', type=int, default=None, help='最大抓取商品数（测试用）')
    parser.add_argument('--delay', type=float, default=0.05, help='请求间隔（秒），默认 0.05')
    parser.add_argument('--db-path', type=str, default=None, help='SQLite 数据库路径')
    parser.add_argument('--full-scrape', action='store_true', help='全量抓取模式（忽略上次抓取时间）')
    parser.add_argument('--state-file', type=str, default=None, help='状态文件路径')
    args = parser.parse_args()
    
    print("="*50)
    print("Lolibrary Scraper v2.0 (优化版)")
    print("="*50)
    
    try:
        scraper = LolibraryScraper(
            delay=args.delay,
            db_path=args.db_path,
            state_file=args.state_file
        )
        
        if args.full_scrape:
            scraper.last_scrape_time = None
            print("\n[MODE] 全量抓取模式")
        
        scraper.scrape(max_items=args.max_items)
        scraper.finish()
        
    except Exception as e:
        print(f"\n[ERROR] 发生错误：{e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
