import sqlite3
import os
import glob

# 清空数据库
db_path = r'C:\Users\Administrator\Documents\db\lolibrary.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute('DELETE FROM lolibrary_images')
cursor.execute('DELETE FROM lolibrary_items')
cursor.execute("DELETE FROM sqlite_sequence WHERE name IN ('lolibrary_items', 'lolibrary_images')")
conn.commit()

# 检查数据是否清空
cursor.execute('SELECT COUNT(*) FROM lolibrary_items')
items = cursor.fetchone()[0]
cursor.execute('SELECT COUNT(*) FROM lolibrary_images')
images = cursor.fetchone()[0]
print(f'数据库已清空: {items} 商品, {images} 图片')

conn.close()

# 删除已下载的图片
image_dir = r'C:\Users\Administrator\Pictures\lolibrary'
if os.path.exists(image_dir):
    files = glob.glob(os.path.join(image_dir, '*'))
    for f in files:
        os.remove(f)
    print(f'图片目录已清空: {len(files)} 个文件')
else:
    os.makedirs(image_dir, exist_ok=True)
    print('图片目录已创建')
