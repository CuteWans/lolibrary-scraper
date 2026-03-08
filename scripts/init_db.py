import sqlite3
import os

db_path = r'C:\Users\Administrator\Documents\db\lolibrary.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 删除旧表
cursor.execute('DROP TABLE IF EXISTS lolibrary_images')
cursor.execute('DROP TABLE IF EXISTS lolibrary_items')
conn.commit()
print('旧表已删除')

# 创建新的商品表（带extra_info字段）
cursor.execute('''
    CREATE TABLE lolibrary_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        url TEXT NOT NULL UNIQUE,
        brand TEXT,
        category TEXT,
        published_at DATETIME,
        scraped_at DATETIME,
        extra_info TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')
print('商品表已创建')

# 创建新的图片表
cursor.execute('''
    CREATE TABLE lolibrary_images (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item_id INTEGER NOT NULL,
        image_url TEXT NOT NULL,
        local_path TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (item_id) REFERENCES lolibrary_items(id) ON DELETE CASCADE
    )
''')
print('图片表已创建')

# 创建索引
cursor.execute('CREATE INDEX idx_items_name ON lolibrary_items(name)')
cursor.execute('CREATE INDEX idx_items_brand ON lolibrary_items(brand)')
cursor.execute('CREATE INDEX idx_items_category ON lolibrary_items(category)')
cursor.execute('CREATE INDEX idx_items_published ON lolibrary_items(published_at)')
cursor.execute('CREATE INDEX idx_images_item_id ON lolibrary_images(item_id)')
print('索引已创建')

conn.commit()

# 验证
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
print('表:', [t[0] for t in cursor.fetchall()])

conn.close()
print('数据库表结构更新完成！')
