---
name: lolibrary-scraper
description: Lolibrary.org 商品图片增量抓取工具（SQLite版本）。用于抓取 https://lolibrary.org/ 网站上新增的Lolita服装商品详情页信息，通过Item Info中的"Published on"时间判断是否为新增商品，只抓取上次执行后新发布的商品。商品和图片分别存储在两个表中，图片表有独立主键ID，支持以图片为粒度的召回。支持直接写入SQLite数据库。使用场景：(1) 需要定期备份Lolibrary新增商品数据，(2) 需要以图片为粒度做召回/检索。
---

# Lolibrary Scraper

Lolibrary.org 商品图片增量抓取工具（SQLite版本）。

## 功能

- **增量抓取**: 只抓取上次执行后新发布的商品
- **图片单独成表**: 每张图片有独立主键ID，支持以图片为粒度的召回
- **SQLite支持**: 可直接写入SQLite数据库
- 自动保存上次抓取时间到状态文件
- 导出为 JSON 和 SQL 格式

## 数据库表结构（SQLite）

### 1. 商品表 `lolibrary_items`

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 主键，自增 |
| name | TEXT | 商品名称 |
| url | TEXT | 详情页URL (UNIQUE) |
| published_at | DATETIME | 商品发布时间 |
| scraped_at | DATETIME | 抓取时间 |
| created_at | TIMESTAMP | 记录创建时间 |
| updated_at | TIMESTAMP | 记录更新时间 |

### 2. 图片表 `lolibrary_images`

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 主键，自增（用于召回） |
| item_id | INTEGER | 关联的商品ID（外键） |
| image_url | TEXT | 图片原始URL |
| created_at | TIMESTAMP | 记录创建时间 |

## 使用方法

### 1. 直接写入SQLite数据库

```bash
cd ~/clawd/skills/lolibrary-scraper
python scripts/scraper.py --db-path "C:/Users/Administrator/Documents/db/lolibrary.db"
```

### 2. 只导出JSON和SQL文件

```bash
python scripts/scraper.py
```

### 3. 完整抓取（所有商品）

```bash
python scripts/scraper.py --db-path "C:/Users/Administrator/Documents/db/lolibrary.db" --full-scrape
```

## 命令行参数

```
python scripts/scraper.py [选项]

选项:
  --max-pages N         最大抓取页数（测试用）
  --max-items N         最大抓取商品数（测试用）
  --delay SECONDS       请求间隔（默认1秒）
  --output-json FILE    JSON输出文件路径
  --output-sql FILE     SQL输出文件路径
  --db-path PATH        SQLite数据库路径（直接写入数据库）
  --state-file FILE     状态文件路径
  --full-scrape         完整抓取模式（忽略上次抓取时间）
```

## SQLite SQL语法说明

本工具生成的SQL文件使用SQLite兼容语法：

### UPSERT (插入或更新)

```sql
-- SQLite 的 UPSERT 语法
INSERT INTO lolibrary_items (name, url, published_at, scraped_at) 
VALUES ('商品名', 'url', '2026-03-07T02:54:00', '2026-03-07T12:00:00')
ON CONFLICT(url) DO UPDATE SET
    name = excluded.name,
    published_at = excluded.published_at,
    scraped_at = excluded.scraped_at;
```

### 插入图片（关联商品）

```sql
-- 使用子查询获取item_id
INSERT INTO lolibrary_images (item_id, image_url)
SELECT id, 'https://.../image.jpg' FROM lolibrary_items 
WHERE url = '商品url';
```

## 图片召回查询示例

### 根据图片ID获取商品信息

```sql
SELECT 
    img.id AS image_id, 
    img.image_url,
    i.id AS item_id, 
    i.name, 
    i.url
FROM lolibrary_images img
JOIN lolibrary_items i ON img.item_id = i.id
WHERE img.id = ?;
```

### 获取最近一周发布的所有图片

```sql
SELECT 
    img.id AS image_id,
    img.image_url,
    i.id AS item_id,
    i.name AS item_name
FROM lolibrary_images img
JOIN lolibrary_items i ON img.item_id = i.id
WHERE i.published_at >= datetime('now', '-7 days')
ORDER BY i.published_at DESC;
```

## 依赖

```bash
pip install requests beautifulsoup4
```

## 输出文件

- `output/lolibrary_data_YYYYMMDD_HHMMSS.json` - JSON格式数据
- `output/lolibrary_data_YYYYMMDD_HHMMSS.sql` - SQLite兼容的SQL文件
- `output/scraper_state.json` - 状态文件（记录上次抓取时间）
