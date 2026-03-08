import sqlite3
import os
import glob

# 清空数据库
db_path = r'C:\Users\Administrator\Documents\db\lolibrary.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 删除所有数据
cursor.execute('DELETE FROM lolibrary_images')
cursor.execute('DELETE FROM lolibrary_items')
cursor.execute("DELETE FROM sqlite_sequence WHERE name IN ('lolibrary_items', 'lolibrary_images')")
conn.commit()

# 验证
cursor.execute('SELECT COUNT(*) FROM lolibrary_items')
items = cursor.fetchone()[0]
cursor.execute('SELECT COUNT(*) FROM lolibrary_images')
images = cursor.fetchone()[0]
print(f'数据库已清空: {items} 商品, {images} 图片')

conn.close()

# 删除所有图片
image_dir = r'C:\Users\Administrator\Pictures\lolibrary'
if os.path.exists(image_dir):
    files = glob.glob(os.path.join(image_dir, '*'))
    for f in files:
        os.remove(f)
    print(f'图片目录已清空: {len(files)} 个文件')

# 删除状态文件
state_file = r'C:\Users\Administrator\clawd\skills\lolibrary-scraper\output\scraper_state.json'
if os.path.exists(state_file):
    os.remove(state_file)
    print('状态文件已删除')

print('\n全部清理完成！')
