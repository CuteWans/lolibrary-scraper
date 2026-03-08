-- Lolibrary.org 商品数据表结构（使用UUID长整数作为主键）

-- 主表：存储商品基本信息
CREATE TABLE IF NOT EXISTS lolibrary_items (
    id INTEGER PRIMARY KEY,        -- UUID生成的64位长整数
    name TEXT NOT NULL,
    url TEXT NOT NULL UNIQUE,      -- 商品URL唯一
    brand TEXT,
    category TEXT,
    published_at DATETIME,
    scraped_at DATETIME,
    extra_info TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 图片表：存储每张图片的信息
CREATE TABLE IF NOT EXISTS lolibrary_images (
    id INTEGER PRIMARY KEY,        -- UUID生成的64位长整数
    item_id INTEGER NOT NULL,      -- 关联的商品ID（UUID长整数）
    image_url TEXT NOT NULL UNIQUE,-- 图片URL唯一
    local_path TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (item_id) REFERENCES lolibrary_items(id) ON DELETE CASCADE
);

-- 索引
CREATE INDEX IF NOT EXISTS idx_items_name ON lolibrary_items(name);
CREATE INDEX IF NOT EXISTS idx_items_brand ON lolibrary_items(brand);
CREATE INDEX IF NOT EXISTS idx_items_category ON lolibrary_items(category);
CREATE INDEX IF NOT EXISTS idx_items_published ON lolibrary_items(published_at);
CREATE INDEX IF NOT EXISTS idx_images_item_id ON lolibrary_images(item_id);
