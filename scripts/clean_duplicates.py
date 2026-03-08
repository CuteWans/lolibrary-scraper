import sqlite3
import os

db_path = r'C:\Users\Administrator\Documents\db\lolibrary.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("开始清理重复数据...")

# 1. 删除重复的图片（保留ID最小的）
cursor.execute('''
    DELETE FROM lolibrary_images 
    WHERE id NOT IN (
        SELECT MIN(id) 
        FROM lolibrary_images 
        GROUP BY image_url
    )
''')
print(f"删除了 {cursor.rowcount} 条重复图片记录")

# 2. 提交更改
conn.commit()

# 3. 检查清理后的数据
cursor.execute('SELECT COUNT(*) FROM lolibrary_images')
print(f"清理后图片总数: {cursor.fetchone()[0]}")

# 4. 检查是否还有重复
cursor.execute('SELECT image_url, COUNT(*) FROM lolibrary_images GROUP BY image_url HAVING COUNT(*) > 1')
duplicates = cursor.fetchall()
print(f"剩余重复图片URL: {len(duplicates)}")

conn.close()
print("数据清理完成！")
