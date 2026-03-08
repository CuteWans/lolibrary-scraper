import sqlite3
import os

db_path = r'C:\Users\Administrator\Documents\db\lolibrary.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 查询商品数量
cursor.execute('SELECT COUNT(*) FROM lolibrary_items')
items_count = cursor.fetchone()[0]
print(f'商品数量: {items_count}')

# 查询图片数量
cursor.execute('SELECT COUNT(*) FROM lolibrary_images')
images_count = cursor.fetchone()[0]
print(f'图片数量: {images_count}')

# 查询前5条商品（带品牌和类目）
cursor.execute('SELECT id, name, brand, category FROM lolibrary_items LIMIT 5')
items = cursor.fetchall()
print('\n前5条商品:')
for item in items:
    name = item[1][:30] if item[1] else ''
    # 避免编码问题，只打印ASCII字符
    name_ascii = name.encode('ascii', 'ignore').decode('ascii')
    brand_ascii = (item[2] or '').encode('ascii', 'ignore').decode('ascii')
    cat_ascii = (item[3] or '').encode('ascii', 'ignore').decode('ascii')
    print(f'  ID:{item[0]} | Brand:{brand_ascii} | Cat:{cat_ascii} | {name_ascii}...')

# 查询前5条图片（带本地路径）
cursor.execute('SELECT id, item_id, local_path FROM lolibrary_images LIMIT 5')
images = cursor.fetchall()
print('\n前5条图片:')
for img in images:
    filename = img[2].split('\\')[-1] if img[2] else 'None'
    print(f'  ImgID:{img[0]} | ItemID:{img[1]} | File:{filename}')

conn.close()

# 检查本地图片文件
image_dir = r'C:\Users\Administrator\Pictures\lolibrary'
if os.path.exists(image_dir):
    files = os.listdir(image_dir)
    print(f'\n本地图片文件数量: {len(files)}')
    print(f'前5个文件名: {files[:5]}')
