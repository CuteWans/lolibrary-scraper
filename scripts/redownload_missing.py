#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
补全缺失图片 - 根据数据库记录下载本地缺失的图片

流程：
1. 从数据库查询所有图片记录（含商品 URL）
2. 检查本地文件是否存在
3. 对缺失的图片，从商品页面重新下载
"""

import sqlite3
import os
import requests
from pathlib import Path
from datetime import datetime
from typing import List, Tuple
import time
from bs4 import BeautifulSoup


def get_missing_images(db_path: str, image_dir: str) -> List[Tuple[int, int, str, str]]:
    """
    获取本地缺失的图片列表
    
    Returns:
        [(image_id, item_id, image_url, item_url), ...]
    """
    print(f"[INFO] 连接数据库：{db_path}")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("[INFO] 查询所有图片记录...")
    cursor.execute('''
        SELECT 
            img.id,
            img.item_id,
            img.image_url,
            i.url as item_url
        FROM lolibrary_images img
        JOIN lolibrary_items i ON img.item_id = i.id
        ORDER BY img.id
    ''')
    
    missing = []
    total = 0
    image_path = Path(image_dir)
    
    for (image_id, item_id, image_url, item_url) in cursor.fetchall():
        total += 1
        if total % 100000 == 0:
            print(f"  已检查 {total} 张图片...")
        
        # 检查本地文件是否存在（尝试不同扩展名）
        file_exists = False
        for ext in ['jpeg', 'jpg', 'png', 'gif', 'webp']:
            local_path = image_path / f"{image_id}.{ext}"
            if local_path.exists():
                file_exists = True
                break
        
        if not file_exists:
            missing.append((image_id, item_id, image_url, item_url))
    
    conn.close()
    
    print(f"[OK] 数据库共 {total} 张图片记录")
    print(f"[WARN] 本地缺失 {len(missing)} 张图片")
    return missing


def get_image_urls_from_item(item_url: str, max_retries: int = 3) -> List[str]:
    """从商品页面提取所有图片 URL"""
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    })
    
    for attempt in range(max_retries):
        try:
            response = session.get(item_url, timeout=30)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            image_urls = []
            images_heading = soup.find('h4', string='Images')
            if images_heading:
                parent = images_heading.parent
                if parent:
                    for link in parent.find_all('a', href=lambda href: href and 'lolibrary.global.ssl.fastly.net/images/' in href):
                        img_url = link.get('href')
                        if img_url and img_url not in image_urls:
                            image_urls.append(img_url)
            
            return image_urls
        except Exception as e:
            print(f"[WARN] 获取商品页面失败 {item_url} (尝试 {attempt + 1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                time.sleep(5)
    
    return []


def download_image(image_url: str, local_path: Path, max_retries: int = 3) -> bool:
    """下载单张图片"""
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    })
    
    for attempt in range(max_retries):
        try:
            response = session.get(image_url, timeout=30)
            response.raise_for_status()
            
            with open(local_path, 'wb') as f:
                f.write(response.content)
            
            return True
        except Exception as e:
            print(f"[WARN] 下载失败 {image_url} (尝试 {attempt + 1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                time.sleep(2)
    
    return False


def redownload_missing(missing: List[Tuple[int, int, str, str]], image_dir: str, delay: float = 0.1) -> Tuple[int, int]:
    """
    重新下载缺失的图片
    
    Returns:
        (success_count, failed_count)
    """
    image_path = Path(image_dir)
    success = 0
    failed = 0
    
    # 按商品分组，避免重复请求同一商品页面
    items_dict = {}
    for (image_id, item_id, image_url, item_url) in missing:
        if item_url not in items_dict:
            items_dict[item_url] = []
        items_dict[item_url].append((image_id, image_url))
    
    print(f"[INFO] 需要访问 {len(items_dict)} 个商品页面")
    
    for idx, (item_url, images) in enumerate(items_dict.items(), 1):
        print(f"\n[{idx}/{len(items_dict)}] 商品：{item_url}")
        print(f"  需要下载 {len(images)} 张图片")
        
        # 获取商品页面的所有图片 URL
        page_images = get_image_urls_from_item(item_url)
        if not page_images:
            print(f"  [ERROR] 无法获取商品页面图片")
            failed += len(images)
            continue
        
        print(f"  [OK] 商品页面找到 {len(page_images)} 张图片")
        
        # 下载每张图片
        for (image_id, expected_url) in images:
            # 尝试从页面找到的图片中匹配
            matched_url = None
            for page_img_url in page_images:
                if expected_url in page_img_url or page_img_url in expected_url:
                    matched_url = page_img_url
                    break
            
            if not matched_url:
                # 如果找不到匹配，尝试直接用原 URL
                matched_url = expected_url
            
            # 尝试不同扩展名
            downloaded = False
            for ext in ['jpeg', 'jpg', 'png', 'gif', 'webp']:
                local_path = image_path / f"{image_id}.{ext}"
                if download_image(matched_url, local_path):
                    print(f"  [OK] {image_id}.{ext}")
                    success += 1
                    downloaded = True
                    break
            
            if not downloaded:
                print(f"  [FAIL] {image_id}")
                failed += 1
            
            time.sleep(delay)
        
        # 商品页面之间延迟
        if idx < len(items_dict):
            time.sleep(delay)
    
    return success, failed


def main():
    import sys
    
    db_path = r"C:\Users\Administrator\Documents\db\lolibrary.db"
    image_dir = r"C:\Users\Administrator\Pictures\lolibrary"
    log_file = r"C:\Users\Administrator\clawd\skills\lolibrary-scraper\output\redownload_log.txt"
    
    # 检查是否自动模式
    auto_mode = '--auto' in sys.argv or '--yes' in sys.argv
    
    print("="*60)
    print("Lolibrary 缺失图片补全工具")
    print("="*60)
    print(f"模式：{'自动下载' if auto_mode else '交互模式'}")
    print()
    
    # 步骤 1: 查找缺失图片
    missing = get_missing_images(db_path, image_dir)
    print()
    
    if not missing:
        print("[OK] 没有缺失图片，数据完全一致！✨")
        return
    
    # 步骤 2: 预览
    print("[INFO] 缺失图片预览（前 20 个）：")
    for (image_id, item_id, image_url, item_url) in missing[:20]:
        print(f"  {image_id} -> {image_url[:60]}...")
    if len(missing) > 20:
        print(f"  ... 还有 {len(missing) - 20} 个")
    print()
    
    # 步骤 3: 写入日志
    Path(log_file).parent.mkdir(parents=True, exist_ok=True)
    with open(log_file, 'w', encoding='utf-8') as f:
        f.write(f"Lolibrary 缺失图片补全日志\n")
        f.write(f"生成时间：{datetime.now().isoformat()}\n")
        f.write(f"运行模式：{'自动下载' if auto_mode else '交互模式'}\n")
        f.write(f"缺失图片数：{len(missing)}\n")
        f.write(f"\n缺失图片列表:\n")
        for (image_id, item_id, image_url, item_url) in missing:
            f.write(f"{image_id}\t{item_id}\t{image_url}\t{item_url}\n")
    
    print(f"[OK] 完整列表已写入日志：{log_file}")
    print()
    
    # 步骤 4: 执行下载
    if auto_mode:
        print(f"\n[INFO] 自动模式：开始下载 {len(missing)} 张缺失图片...")
        success, failed = redownload_missing(missing, image_dir)
        
        print(f"\n{'='*60}")
        print(f"[OK] 下载完成！成功：{success}, 失败：{failed}")
        print(f"{'='*60}")
        
        # 更新日志
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(f"\n\n下载结果:\n")
            f.write(f"成功下载：{success}\n")
            f.write(f"下载失败：{failed}\n")
            f.write(f"完成时间：{datetime.now().isoformat()}\n")
    else:
        # 交互模式：询问是否下载
        try:
            response = input(f"\n是否重新下载这 {len(missing)} 张缺失图片？(yes/no): ").strip().lower()
            if response != 'yes':
                print("\n[INFO] 已取消下载操作")
                return
            
            # 执行下载
            print(f"\n[INFO] 开始下载缺失图片...")
            success, failed = redownload_missing(missing, image_dir)
            
            print(f"\n{'='*60}")
            print(f"[OK] 下载完成！成功：{success}, 失败：{failed}")
            print(f"{'='*60}")
            
            # 更新日志
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(f"\n\n下载结果:\n")
                f.write(f"成功下载：{success}\n")
                f.write(f"下载失败：{failed}\n")
                f.write(f"完成时间：{datetime.now().isoformat()}\n")
        except EOFError:
            print("\n[ERROR] 无法读取用户输入，请使用 --auto 参数运行")


if __name__ == '__main__':
    main()
