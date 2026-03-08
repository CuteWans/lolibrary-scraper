#!/usr/bin/env python3
"""
修复孤儿图片：找出本地有但数据库没有的图片记录
"""

import sqlite3
import os
from pathlib import Path

DB_PATH = r"C:\Users\Administrator\Documents\db\lolibrary.db"
IMAGE_DIR = Path(r"C:\Users\Administrator\Pictures\lolibrary")

def main():
    # 连接数据库
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 获取数据库中所有图片的 local_path
    cursor.execute("SELECT local_path FROM lolibrary_images WHERE local_path IS NOT NULL")
    db_paths = set(row[0] for row in cursor.fetchall())
    
    # 获取本地所有图片文件
    local_files = set()
    for f in IMAGE_DIR.iterdir():
        if f.is_file():
            local_files.add(str(f))
    
    # 找出本地有但数据库没有的图片
    orphan_files = local_files - db_paths
    
    print(f"数据库图片记录：{len(db_paths)}")
    print(f"本地图片文件：{len(local_files)}")
    print(f"孤儿图片数量：{len(orphan_files)}")
    
    if orphan_files:
        print("\n前 10 个孤儿图片:")
        for f in list(orphan_files)[:10]:
            print(f"  {f}")
    
    # 获取数据库中所有的 image_id（从 local_path 提取）
    db_ids = set()
    for path in db_paths:
        filename = os.path.basename(path)
        image_id = os.path.splitext(filename)[0]
        db_ids.add(image_id)
    
    # 本地文件 ID
    local_ids = set()
    for f in local_files:
        filename = os.path.basename(f)
        image_id = os.path.splitext(filename)[0]
        local_ids.add(image_id)
    
    # 找出本地有但数据库没有的 ID
    orphan_ids = local_ids - db_ids
    
    print(f"\n孤儿图片 ID 数量：{len(orphan_ids)}")
    if orphan_ids:
        print("前 10 个孤儿 ID:")
        for id_ in list(orphan_ids)[:10]:
            print(f"  {id_}")
    
    conn.close()

if __name__ == "__main__":
    main()
