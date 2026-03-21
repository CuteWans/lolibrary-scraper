#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
清理孤儿图片文件 - 删除本地存在但数据库中没有记录的图片

安全模式：
1. 先列出所有待删除文件
2. 确认后批量删除
3. 记录删除日志
"""

import sqlite3
import os
from pathlib import Path
from datetime import datetime


def get_db_image_ids(db_path: str) -> set:
    """从数据库获取所有图片 ID"""
    print(f"[INFO] 连接数据库：{db_path}")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("[INFO] 查询数据库中的图片 ID...")
    cursor.execute("SELECT id FROM lolibrary_images")
    
    db_ids = set()
    for (id_,) in cursor.fetchall():
        db_ids.add(id_)
    
    conn.close()
    print(f"[OK] 数据库中共有 {len(db_ids)} 张图片记录")
    return db_ids


def get_local_image_files(image_dir: str) -> dict:
    """获取本地所有图片文件 {文件名: 完整路径}"""
    print(f"[INFO] 扫描本地目录：{image_dir}")
    image_path = Path(image_dir)
    
    local_files = {}
    count = 0
    for file in image_path.iterdir():
        if file.is_file():
            # 文件名去掉扩展名作为 ID
            file_id = int(file.stem)
            local_files[file_id] = str(file)
            count += 1
            if count % 100000 == 0:
                print(f"  已扫描 {count} 个文件...")
    
    print(f"[OK] 本地目录共有 {len(local_files)} 个图片文件")
    return local_files


def find_orphans(db_ids: set, local_files: dict) -> list:
    """找出本地有但数据库没有的孤儿文件"""
    print("[INFO] 对比查找孤儿文件...")
    
    orphans = []
    for file_id, file_path in local_files.items():
        if file_id not in db_ids:
            orphans.append((file_id, file_path))
    
    print(f"[WARN] 找到 {len(orphans)} 个孤儿文件")
    return orphans


def delete_orphans(orphans: list, dry_run: bool = True) -> tuple:
    """
    删除孤儿文件
    
    Args:
        orphans: [(id, path), ...]
        dry_run: True=只预览不删除，False=实际删除
    
    Returns:
        (deleted_count, failed_count, error_list)
    """
    deleted = 0
    failed = 0
    errors = []
    
    for file_id, file_path in orphans:
        try:
            if dry_run:
                print(f"  [DRY] 待删除：{file_id} -> {file_path}")
            else:
                os.remove(file_path)
                deleted += 1
                if deleted % 1000 == 0:
                    print(f"  已删除 {deleted} 个文件...")
        except Exception as e:
            failed += 1
            errors.append((file_id, file_path, str(e)))
            print(f"  [ERROR] 删除失败 {file_id}: {e}")
    
    return deleted, failed, errors


def main():
    import sys
    
    db_path = r"C:\Users\Administrator\Documents\db\lolibrary.db"
    image_dir = r"C:\Users\Administrator\Pictures\lolibrary"
    log_file = r"C:\Users\Administrator\clawd\skills\lolibrary-scraper\output\cleanup_log.txt"
    
    # 检查是否直接删除模式
    auto_delete = '--delete' in sys.argv or '--auto' in sys.argv
    
    print("="*60)
    print("Lolibrary 孤儿图片清理工具")
    print("="*60)
    print(f"模式：{'自动删除' if auto_delete else '预览模式'}")
    print()
    
    # 步骤 1: 获取数据库 ID
    db_ids = get_db_image_ids(db_path)
    print()
    
    # 步骤 2: 获取本地文件
    local_files = get_local_image_files(image_dir)
    print()
    
    # 步骤 3: 查找孤儿
    orphans = find_orphans(db_ids, local_files)
    print()
    
    if not orphans:
        print("[OK] 没有发现孤儿文件，数据一致性良好！✨")
        return
    
    # 步骤 4: 预览待删除文件（前 20 个）
    print("[INFO] 待删除文件预览（前 20 个）：")
    for file_id, file_path in orphans[:20]:
        print(f"  {file_id} -> {file_path}")
    if len(orphans) > 20:
        print(f"  ... 还有 {len(orphans) - 20} 个文件")
    print()
    
    # 步骤 5: 写入日志
    Path(log_file).parent.mkdir(parents=True, exist_ok=True)
    with open(log_file, 'w', encoding='utf-8') as f:
        f.write(f"Lolibrary 孤儿图片清理日志\n")
        f.write(f"生成时间：{datetime.now().isoformat()}\n")
        f.write(f"数据库路径：{db_path}\n")
        f.write(f"图片目录：{image_dir}\n")
        f.write(f"运行模式：{'自动删除' if auto_delete else '预览模式'}\n")
        f.write(f"\n数据库图片数：{len(db_ids)}\n")
        f.write(f"本地文件数：{len(local_files)}\n")
        f.write(f"孤儿文件数：{len(orphans)}\n")
        f.write(f"\n待删除文件列表:\n")
        for file_id, file_path in orphans:
            f.write(f"{file_id}\t{file_path}\n")
    
    print(f"[OK] 完整列表已写入日志：{log_file}")
    print()
    
    # 步骤 6: 执行删除
    if auto_delete:
        print(f"\n[INFO] 自动删除模式：开始删除 {len(orphans)} 个孤儿文件...")
        deleted, failed, errors = delete_orphans(orphans, dry_run=False)
        print(f"\n[OK] 删除完成！成功：{deleted}, 失败：{failed}")
        
        # 更新日志
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(f"\n\n删除结果:\n")
            f.write(f"成功删除：{deleted}\n")
            f.write(f"删除失败：{failed}\n")
            f.write(f"完成时间：{datetime.now().isoformat()}\n")
            if errors:
                f.write(f"\n错误详情:\n")
                for file_id, file_path, error in errors:
                    f.write(f"{file_id}\t{file_path}\t{error}\n")
    else:
        # 预览模式：询问是否删除
        if len(orphans) <= 100:
            response = input(f"\n是否删除这 {len(orphans)} 个孤儿文件？(yes/no): ").strip().lower()
            if response == 'yes':
                print("\n[INFO] 开始删除孤儿文件...")
                deleted, failed, errors = delete_orphans(orphans, dry_run=False)
                print(f"\n[OK] 删除完成！成功：{deleted}, 失败：{failed}")
                
                # 更新日志
                with open(log_file, 'a', encoding='utf-8') as f:
                    f.write(f"\n\n删除结果:\n")
                    f.write(f"成功删除：{deleted}\n")
                    f.write(f"删除失败：{failed}\n")
                    f.write(f"完成时间：{datetime.now().isoformat()}\n")
            else:
                print("\n[INFO] 已取消删除操作")
        else:
            print(f"\n[INFO] 孤儿文件数量较多 ({len(orphans)} 个)")
            print("请使用 --delete 参数执行自动删除：")
            print(f"  python scripts/cleanup_orphans.py --delete")


if __name__ == '__main__':
    main()
