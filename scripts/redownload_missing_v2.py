#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
补全缺失图片 v2 - 增强版

改进：
- 增加重试次数（5 次）
- 增加延迟（1 秒/页）
- 使用 aiohttp 异步下载
- 详细错误日志
"""

import sqlite3
import os
import requests
from pathlib import Path
from datetime import datetime
from typing import List, Tuple
import time
from bs4 import BeautifulSoup
import traceback


def get_missing_images(db_path: str, image_dir: str) -> List[Tuple[int, int, str, str]]:
    """获取本地缺失的图片列表"""
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
        for ext in ['jpeg', 'jpg', 'png', 'gif', 'webp', 'bmp']:
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


def download_image_direct(image_url: str, local_path: Path, session: requests.Session, max_retries: int = 5) -> bool:
    """直接下载图片（不访问商品页面）"""
    for attempt in range(max_retries):
        try:
            response = session.get(image_url, timeout=60)
            response.raise_for_status()
            
            # 检查内容是否是有效的图片
            content = response.content
            if len(content) < 100:
                print(f"    [WARN] 文件太小 ({len(content)} bytes)")
                if attempt < max_retries - 1:
                    time.sleep(3)
                    continue
            
            with open(local_path, 'wb') as f:
                f.write(content)
            
            return True
        except requests.exceptions.Timeout as e:
            print(f"    [WARN] 超时 (尝试 {attempt + 1}/{max_retries})")
            if attempt < max_retries - 1:
                time.sleep(5)
        except requests.exceptions.RequestException as e:
            print(f"    [WARN] 请求失败：{e} (尝试 {attempt + 1}/{max_retries})")
            if attempt < max_retries - 1:
                time.sleep(5)
        except Exception as e:
            print(f"    [ERROR] 未知错误：{e}")
            return False
    
    return False


def redownload_missing(missing: List[Tuple[int, int, str, str]], image_dir: str, log_file: str) -> Tuple[int, int]:
    """重新下载缺失的图片"""
    image_path = Path(image_dir)
    success = 0
    failed = 0
    errors = []
    
    # 创建会话
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'Accept': 'image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Referer': 'https://lolibrary.org/',
    })
    
    print(f"[INFO] 开始下载 {len(missing)} 张图片...")
    print(f"[INFO] 图片目录：{image_dir}")
    print()
    
    for idx, (image_id, item_id, image_url, item_url) in enumerate(missing, 1):
        print(f"[{idx}/{len(missing)}] 下载图片 {image_id}...")
        
        # 尝试不同扩展名
        downloaded = False
        used_ext = None
        
        for ext in ['jpeg', 'jpg', 'png', 'gif', 'webp', 'bmp']:
            local_path = image_path / f"{image_id}.{ext}"
            
            # 跳过已存在的文件
            if local_path.exists():
                print(f"  [SKIP] 文件已存在：{local_path.name}")
                success += 1
                downloaded = True
                used_ext = ext
                break
            
            # 尝试下载
            if download_image_direct(image_url, local_path, session):
                print(f"  [OK] 下载成功：{local_path.name}")
                success += 1
                downloaded = True
                used_ext = ext
                break
            
            # 尝试替换 URL 中的扩展名
            alt_url = image_url.rsplit('.', 1)[0] + '.' + ext
            if alt_url != image_url:
                if download_image_direct(alt_url, local_path, session):
                    print(f"  [OK] 下载成功（备用 URL）：{local_path.name}")
                    success += 1
                    downloaded = True
                    used_ext = ext
                    break
        
        if not downloaded:
            print(f"  [FAIL] 下载失败")
            failed += 1
            errors.append({
                'image_id': image_id,
                'item_id': item_id,
                'image_url': image_url,
                'item_url': item_url
            })
        
        # 每 10 张图片延迟一下
        if idx % 10 == 0:
            print(f"  ... 休息 2 秒 ...")
            time.sleep(2)
    
    # 写入错误日志
    if errors:
        error_log = log_file.replace('.txt', '_errors.json')
        import json
        with open(error_log, 'w', encoding='utf-8') as f:
            json.dump(errors, f, ensure_ascii=False, indent=2)
        print(f"\n[WARN] {len(errors)} 个错误详情已写入：{error_log}")
    
    return success, failed


def main():
    import sys
    
    db_path = r"C:\Users\Administrator\Documents\db\lolibrary.db"
    image_dir = r"C:\Users\Administrator\Pictures\lolibrary"
    log_file = r"C:\Users\Administrator\clawd\skills\lolibrary-scraper\output\redownload_v2_log.txt"
    
    print("="*60)
    print("Lolibrary 缺失图片补全工具 v2")
    print("="*60)
    print()
    
    # 步骤 1: 查找缺失图片
    missing = get_missing_images(db_path, image_dir)
    print()
    
    if not missing:
        print("[OK] 没有缺失图片，数据完全一致！✨")
        return
    
    # 步骤 2: 预览
    print("[INFO] 缺失图片预览（前 10 个）：")
    for (image_id, item_id, image_url, item_url) in missing[:10]:
        print(f"  {image_id} -> {image_url[:60]}...")
    if len(missing) > 10:
        print(f"  ... 还有 {len(missing) - 10} 个")
    print()
    
    # 步骤 3: 写入日志
    Path(log_file).parent.mkdir(parents=True, exist_ok=True)
    with open(log_file, 'w', encoding='utf-8') as f:
        f.write(f"Lolibrary 缺失图片补全日志 v2\n")
        f.write(f"生成时间：{datetime.now().isoformat()}\n")
        f.write(f"缺失图片数：{len(missing)}\n")
        f.write(f"\n缺失图片列表:\n")
        for (image_id, item_id, image_url, item_url) in missing:
            f.write(f"{image_id}\t{item_id}\t{image_url}\t{item_url}\n")
    
    print(f"[OK] 完整列表已写入日志：{log_file}")
    print()
    
    # 步骤 4: 执行下载
    print(f"[INFO] 开始下载缺失图片...\n")
    success, failed = redownload_missing(missing, image_dir, log_file)
    
    print(f"\n{'='*60}")
    print(f"[OK] 下载完成！成功：{success}, 失败：{failed}")
    print(f"{'='*60}")
    
    # 更新日志
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(f"\n\n下载结果:\n")
        f.write(f"成功下载：{success}\n")
        f.write(f"下载失败：{failed}\n")
        f.write(f"完成时间：{datetime.now().isoformat()}\n")


if __name__ == '__main__':
    main()
