import sqlite3
import json

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

# 查询第一条商品的 extra_info
cursor.execute('SELECT id, name, brand, category, extra_info FROM lolibrary_items LIMIT 1')
item = cursor.fetchone()
print(f'\n商品ID: {item[0]}')
name_ascii = item[1].encode('ascii', 'ignore').decode('ascii') if item[1] else ''
brand_ascii = item[2].encode('ascii', 'ignore').decode('ascii') if item[2] else ''
cat_ascii = item[3].encode('ascii', 'ignore').decode('ascii') if item[3] else ''
print(f'名称: {name_ascii}')
print(f'品牌: {brand_ascii}')
print(f'类目: {cat_ascii}')
print(f'\nExtra Info (JSON):')
if item[4]:
    extra = json.loads(item[4])
    for key, value in extra.items():
        print(f'  {key}: {value}')
else:
    print('  None')

# 查询第二条商品（有更多尺寸信息）
cursor.execute('SELECT id, name, extra_info FROM lolibrary_items WHERE id = 3')
item2 = cursor.fetchone()
if item2:
    name2_ascii = item2[1].encode('ascii', 'ignore').decode('ascii') if item2[1] else ''
    print(f'\n商品ID: {item2[0]} - {name2_ascii}')
    print('Extra Info:')
    if item2[2]:
        extra2 = json.loads(item2[2])
        for key, value in extra2.items():
            print(f'  {key}: {value}')

conn.close()
