import sqlite3
import os
import glob

# 删除数据库文件
db_path = r'C:\Users\Administrator\Documents\db\lolibrary.db'
if os.path.exists(db_path):
    os.remove(db_path)
    print(f'数据库已删除: {db_path}')

# 删除所有图片
image_dir = r'C:\Users\Administrator\Pictures\lolibrary'
if os.path.exists(image_dir):
    files = glob.glob(os.path.join(image_dir, '*'))
    for f in files:
        os.remove(f)
    print(f'图片目录已清空: {len(files)} 个文件')
else:
    os.makedirs(image_dir, exist_ok=True)
    print('图片目录已创建')

# 删除状态文件
state_file = r'C:\Users\Administrator\clawd\skills\lolibrary-scraper\output\scraper_state.json'
if os.path.exists(state_file):
    os.remove(state_file)
    print(f'状态文件已删除: {state_file}')

print('\n全部清理完成！')
