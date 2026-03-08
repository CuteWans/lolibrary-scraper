PRAGMA foreign_keys = ON;

-- 插入/更新商品: Cherry Kitty JSK체리 키티...
INSERT INTO lolibrary_items (name, url, brand, category, published_at, scraped_at, extra_info) 
VALUES ('Cherry Kitty JSK체리 키티', 'https://lolibrary.org/items/haenuli-cherry-kitty-jsk', 'Haenuli', 'JSK', '2026-03-07T07:13:42+00:00', '2026-03-07T07:23:06.842730+00:00', '{"Brand": "Haenuli", "Category": "JSK", "Features": ["Corset Lacing", "Detachable Bow", "Partial Shirring", "Pintucks", "Side Zip"], "Colorways": "Red", "Tags": ["Cats", "Florals", "Pattern: Polka Dots", "Sanrio"]}')
ON CONFLICT(url) DO UPDATE SET
    name = excluded.name,
    brand = excluded.brand,
    category = excluded.category,
    published_at = excluded.published_at,
    scraped_at = excluded.scraped_at,
    extra_info = excluded.extra_info;

-- 插入图片
INSERT INTO lolibrary_images (item_id, image_url)
SELECT id, 'https://lolibrary.global.ssl.fastly.net/images/3CUtx4Ch8Zl71hXcu9XOPbU3ktkKje671j1kUd6B.jpeg' FROM lolibrary_items WHERE url = 'https://lolibrary.org/items/haenuli-cherry-kitty-jsk';

-- 插入图片
INSERT INTO lolibrary_images (item_id, image_url)
SELECT id, 'https://lolibrary.global.ssl.fastly.net/images/UMj7iHhQJsFdYHLltp3g2OaDxW5FyfvXDrlrC2XN.jpeg' FROM lolibrary_items WHERE url = 'https://lolibrary.org/items/haenuli-cherry-kitty-jsk';

-- 插入图片
INSERT INTO lolibrary_images (item_id, image_url)
SELECT id, 'https://lolibrary.global.ssl.fastly.net/images/w2Fan52VY28GCRb0MSs50pGAc3gPjzIKAievoXVX.jpeg' FROM lolibrary_items WHERE url = 'https://lolibrary.org/items/haenuli-cherry-kitty-jsk';

-- 插入图片
INSERT INTO lolibrary_images (item_id, image_url)
SELECT id, 'https://lolibrary.global.ssl.fastly.net/images/lZ8C2UIJoAjGQzLInj5LVaFENs5JLY3XmsoWweW0.jpeg' FROM lolibrary_items WHERE url = 'https://lolibrary.org/items/haenuli-cherry-kitty-jsk';

-- 插入图片
INSERT INTO lolibrary_images (item_id, image_url)
SELECT id, 'https://lolibrary.global.ssl.fastly.net/images/pHbLCpw0QNLmloj4bIGjcarids8G5VIH6r4zAzKQ.jpeg' FROM lolibrary_items WHERE url = 'https://lolibrary.org/items/haenuli-cherry-kitty-jsk';

-- 插入/更新商品: A Faint Day JSK아련한 그날...
INSERT INTO lolibrary_items (name, url, brand, category, published_at, scraped_at, extra_info) 
VALUES ('A Faint Day JSK아련한 그날', 'https://lolibrary.org/items/haenuli-a-faint-day-jsk', 'Haenuli', 'JSK', '2026-03-07T07:04:01+00:00', '2026-03-07T07:23:09.008742+00:00', '{"Brand": "Haenuli", "Category": "JSK", "Features": ["Back Zip", "High Neck Collar", "No Shirring"], "Colorways": "Blue", "Tags": ["Florals", "Pattern: Stripes"]}')
ON CONFLICT(url) DO UPDATE SET
    name = excluded.name,
    brand = excluded.brand,
    category = excluded.category,
    published_at = excluded.published_at,
    scraped_at = excluded.scraped_at,
    extra_info = excluded.extra_info;

-- 插入图片
INSERT INTO lolibrary_images (item_id, image_url)
SELECT id, 'https://lolibrary.global.ssl.fastly.net/images/YmzD9o0TRBtD1jxfFJh6IjKccYlXOtg80juI9IDA.jpeg' FROM lolibrary_items WHERE url = 'https://lolibrary.org/items/haenuli-a-faint-day-jsk';

-- 插入图片
INSERT INTO lolibrary_images (item_id, image_url)
SELECT id, 'https://lolibrary.global.ssl.fastly.net/images/ltXh1mmeN7Xyp5ovXXpky6JQc6WzoOulXOBr45Ka.jpeg' FROM lolibrary_items WHERE url = 'https://lolibrary.org/items/haenuli-a-faint-day-jsk';

-- 插入图片
INSERT INTO lolibrary_images (item_id, image_url)
SELECT id, 'https://lolibrary.global.ssl.fastly.net/images/88ReXdvys6qT49VS7yXNJe3mv1vs8guFnkr6jmQC.jpeg' FROM lolibrary_items WHERE url = 'https://lolibrary.org/items/haenuli-a-faint-day-jsk';

-- 插入图片
INSERT INTO lolibrary_images (item_id, image_url)
SELECT id, 'https://lolibrary.global.ssl.fastly.net/images/898h4rWXUxC807QrJjQIZQpPrX5BjIevAX0gH9xn.jpeg' FROM lolibrary_items WHERE url = 'https://lolibrary.org/items/haenuli-a-faint-day-jsk';

-- 插入图片
INSERT INTO lolibrary_images (item_id, image_url)
SELECT id, 'https://lolibrary.global.ssl.fastly.net/images/jK6w3JtQ294Zo8w2H8q8kmoGzv0kkV9Jc2f3j1o6.jpeg' FROM lolibrary_items WHERE url = 'https://lolibrary.org/items/haenuli-a-faint-day-jsk';

-- 插入图片
INSERT INTO lolibrary_images (item_id, image_url)
SELECT id, 'https://lolibrary.global.ssl.fastly.net/images/7YfADz7jwNnTixv097vXR1xCFZEx8XFzncfte6vY.jpeg' FROM lolibrary_items WHERE url = 'https://lolibrary.org/items/haenuli-a-faint-day-jsk';

-- 插入/更新商品: Lady Charlotte OP...
INSERT INTO lolibrary_items (name, url, brand, category, published_at, scraped_at, extra_info) 
VALUES ('Lady Charlotte OP', 'https://lolibrary.org/items/haenuli-lady-charlotte-op', 'Haenuli', 'OP', '2026-03-07T05:40:02+00:00', '2026-03-07T07:23:11.256685+00:00', '{"Bust": "41.5 cm (flat)", "Length": "97 cm", "Shoulder Width": "34 cm", "Sleeve Length": "70 cm", "Waist": "33.5 cm (flat)", "Brand": "Haenuli", "Category": "OP", "Features": ["Buttoned Cuffs", "Long Sleeves", "No Shirring", "Peter Pan Collar"], "Colorways": "Blue", "Tags": "Pattern: Stripes"}')
ON CONFLICT(url) DO UPDATE SET
    name = excluded.name,
    brand = excluded.brand,
    category = excluded.category,
    published_at = excluded.published_at,
    scraped_at = excluded.scraped_at,
    extra_info = excluded.extra_info;

-- 插入图片
INSERT INTO lolibrary_images (item_id, image_url)
SELECT id, 'https://lolibrary.global.ssl.fastly.net/images/hOi1poTRKohtmtg4ivlONe5nP5yLL6uDTOMNcRQC.jpeg' FROM lolibrary_items WHERE url = 'https://lolibrary.org/items/haenuli-lady-charlotte-op';

-- 插入图片
INSERT INTO lolibrary_images (item_id, image_url)
SELECT id, 'https://lolibrary.global.ssl.fastly.net/images/twnNN4uaarTzJOLjWbTZNKFzdKg9d79eVbZ5Dipf.jpeg' FROM lolibrary_items WHERE url = 'https://lolibrary.org/items/haenuli-lady-charlotte-op';

-- 插入图片
INSERT INTO lolibrary_images (item_id, image_url)
SELECT id, 'https://lolibrary.global.ssl.fastly.net/images/F7c4fOhbfQCEX4WFWRGfbATGp28mVuxsntL7sGsg.jpeg' FROM lolibrary_items WHERE url = 'https://lolibrary.org/items/haenuli-lady-charlotte-op';

-- 插入图片
INSERT INTO lolibrary_images (item_id, image_url)
SELECT id, 'https://lolibrary.global.ssl.fastly.net/images/fBuTNZOcrKXhVKCOw0qzXVsGMOLGkxeCNZb00IgA.jpeg' FROM lolibrary_items WHERE url = 'https://lolibrary.org/items/haenuli-lady-charlotte-op';

-- 插入图片
INSERT INTO lolibrary_images (item_id, image_url)
SELECT id, 'https://lolibrary.global.ssl.fastly.net/images/ONjLQPbxcaCohTjWC8cIiW11xqGdhoUjzigWgGkw.jpeg' FROM lolibrary_items WHERE url = 'https://lolibrary.org/items/haenuli-lady-charlotte-op';

-- 插入图片
INSERT INTO lolibrary_images (item_id, image_url)
SELECT id, 'https://lolibrary.global.ssl.fastly.net/images/BnYqICzkTK0BVl4aoUo85FASxp5kPB1bxv5OhC5W.jpeg' FROM lolibrary_items WHERE url = 'https://lolibrary.org/items/haenuli-lady-charlotte-op';

-- 插入/更新商品: Fairy Angel OP...
INSERT INTO lolibrary_items (name, url, brand, category, published_at, scraped_at, extra_info) 
VALUES ('Fairy Angel OP', 'https://lolibrary.org/items/haenuli-fairy-angel-op', 'Haenuli', 'OP', '2026-03-07T05:31:53+00:00', '2026-03-07T07:23:13.435653+00:00', '{"Bust": "43 cm (flat)", "Length": "90 cm", "Shoulder Width": "32 cm", "Sleeve Length": "21.5 cm", "Waist": "35 cm", "Brand": "Haenuli", "Category": "OP", "Features": ["Back Zip", "Elasticized Cuffs", "Neck ties", "No Shirring", "Removable Sash", "Short Sleeves"], "Colorways": "Sax", "Tags": ["Fairies", "Florals"]}')
ON CONFLICT(url) DO UPDATE SET
    name = excluded.name,
    brand = excluded.brand,
    category = excluded.category,
    published_at = excluded.published_at,
    scraped_at = excluded.scraped_at,
    extra_info = excluded.extra_info;

-- 插入图片
INSERT INTO lolibrary_images (item_id, image_url)
SELECT id, 'https://lolibrary.global.ssl.fastly.net/images/q9Xo4idQDiTPz38alqfunLhfm9djF8oR4iLe8jhw.jpeg' FROM lolibrary_items WHERE url = 'https://lolibrary.org/items/haenuli-fairy-angel-op';

-- 插入图片
INSERT INTO lolibrary_images (item_id, image_url)
SELECT id, 'https://lolibrary.global.ssl.fastly.net/images/UVmBJbUUX3hr8ID2iJW2RwQ3dOX9ZaapfP3ShRzk.jpeg' FROM lolibrary_items WHERE url = 'https://lolibrary.org/items/haenuli-fairy-angel-op';

-- 插入图片
INSERT INTO lolibrary_images (item_id, image_url)
SELECT id, 'https://lolibrary.global.ssl.fastly.net/images/WHK51cJGnjD1yIxL3Pp5cNwBkkXDdvOdgpWIb62g.jpeg' FROM lolibrary_items WHERE url = 'https://lolibrary.org/items/haenuli-fairy-angel-op';

-- 插入图片
INSERT INTO lolibrary_images (item_id, image_url)
SELECT id, 'https://lolibrary.global.ssl.fastly.net/images/fcKOnwwyqLAzkT9QAet4uXjDfJe1V5Reoo2WRtnX.jpeg' FROM lolibrary_items WHERE url = 'https://lolibrary.org/items/haenuli-fairy-angel-op';

-- 插入/更新商品: Classic Flower JSK...
INSERT INTO lolibrary_items (name, url, brand, category, published_at, scraped_at, extra_info) 
VALUES ('Classic Flower JSK', 'https://lolibrary.org/items/haenuli-classic-flower-jsk', 'Haenuli', 'JSK', '2026-03-07T05:12:23+00:00', '2026-03-07T07:23:15.511365+00:00', '{"Bust": "39-47 cm (flat)", "Length": "83 cm", "Waist": "33-44 cm", "Brand": "Haenuli", "Category": "JSK", "Features": ["Corset Lacing", "Dropped Waist", "Elasticized Cuffs", "Side Zip"], "Colorways": ["Purple", "Wine/Bordeaux"], "Tags": ["Florals", "Roses"]}')
ON CONFLICT(url) DO UPDATE SET
    name = excluded.name,
    brand = excluded.brand,
    category = excluded.category,
    published_at = excluded.published_at,
    scraped_at = excluded.scraped_at,
    extra_info = excluded.extra_info;

-- 插入图片
INSERT INTO lolibrary_images (item_id, image_url)
SELECT id, 'https://lolibrary.global.ssl.fastly.net/images/KbhkuA4tCvbbncYEB08DjjruvHHqGLKZETGseSKJ.jpeg' FROM lolibrary_items WHERE url = 'https://lolibrary.org/items/haenuli-classic-flower-jsk';

-- 插入图片
INSERT INTO lolibrary_images (item_id, image_url)
SELECT id, 'https://lolibrary.global.ssl.fastly.net/images/0NcQEGYvRtFxAKEp8bzkYm3EnAQj4k3ldsaxy3NB.jpeg' FROM lolibrary_items WHERE url = 'https://lolibrary.org/items/haenuli-classic-flower-jsk';

-- 插入图片
INSERT INTO lolibrary_images (item_id, image_url)
SELECT id, 'https://lolibrary.global.ssl.fastly.net/images/VgregnYqZnxuoZ1MSPs3hdEARlGKbAGnVfZFG0Uv.jpeg' FROM lolibrary_items WHERE url = 'https://lolibrary.org/items/haenuli-classic-flower-jsk';

-- 插入图片
INSERT INTO lolibrary_images (item_id, image_url)
SELECT id, 'https://lolibrary.global.ssl.fastly.net/images/DfG3h6iB7f6dPBvggARhJKjLU5AJ86uoY5EOCjrs.jpeg' FROM lolibrary_items WHERE url = 'https://lolibrary.org/items/haenuli-classic-flower-jsk';

-- 插入图片
INSERT INTO lolibrary_images (item_id, image_url)
SELECT id, 'https://lolibrary.global.ssl.fastly.net/images/5Jte2Q2lrPpO3S5jymQn05XdufIKI5Vsvpzc5Juh.jpeg' FROM lolibrary_items WHERE url = 'https://lolibrary.org/items/haenuli-classic-flower-jsk';

-- 插入图片
INSERT INTO lolibrary_images (item_id, image_url)
SELECT id, 'https://lolibrary.global.ssl.fastly.net/images/IFK01qRgTH8Yr36w7hpbAEvsxPaCLTJaOj6kgB9I.jpeg' FROM lolibrary_items WHERE url = 'https://lolibrary.org/items/haenuli-classic-flower-jsk';

-- 插入图片
INSERT INTO lolibrary_images (item_id, image_url)
SELECT id, 'https://lolibrary.global.ssl.fastly.net/images/BsOQ1v3tK17JoJMeEqFb2BNidhicC7rBLw903WVX.jpeg' FROM lolibrary_items WHERE url = 'https://lolibrary.org/items/haenuli-classic-flower-jsk';

-- 插入图片
INSERT INTO lolibrary_images (item_id, image_url)
SELECT id, 'https://lolibrary.global.ssl.fastly.net/images/iDsEh2wPkAJHjFQ4xqrQzIwt0KNNJAhCSlEIcNXU.jpeg' FROM lolibrary_items WHERE url = 'https://lolibrary.org/items/haenuli-classic-flower-jsk';

-- 插入图片
INSERT INTO lolibrary_images (item_id, image_url)
SELECT id, 'https://lolibrary.global.ssl.fastly.net/images/du1Z66WlRTHByB3vTQhUmU3Y0EF8iyVc77A53IOQ.jpeg' FROM lolibrary_items WHERE url = 'https://lolibrary.org/items/haenuli-classic-flower-jsk';

-- 插入图片
INSERT INTO lolibrary_images (item_id, image_url)
SELECT id, 'https://lolibrary.global.ssl.fastly.net/images/t11ny6dwXnM2s7oiv8JDs4DD03fDYyS1dblJzBMT.jpeg' FROM lolibrary_items WHERE url = 'https://lolibrary.org/items/haenuli-classic-flower-jsk';

-- 插入图片
INSERT INTO lolibrary_images (item_id, image_url)
SELECT id, 'https://lolibrary.global.ssl.fastly.net/images/PLVsH4jCzV2z5Uw2nog50SmfijEVL0vmwuqXUqiC.jpeg' FROM lolibrary_items WHERE url = 'https://lolibrary.org/items/haenuli-classic-flower-jsk';

-- 插入图片
INSERT INTO lolibrary_images (item_id, image_url)
SELECT id, 'https://lolibrary.global.ssl.fastly.net/images/ffZomt4fTwvYDUpSgkZLJcZwDyUL4jHpE5QilF0B.jpeg' FROM lolibrary_items WHERE url = 'https://lolibrary.org/items/haenuli-classic-flower-jsk';

-- 插入/更新商品: Misty Violet JSK...
INSERT INTO lolibrary_items (name, url, brand, category, published_at, scraped_at, extra_info) 
VALUES ('Misty Violet JSK', 'https://lolibrary.org/items/haenuli-misty-violet-jsk', 'Haenuli', 'JSK', '2026-03-07T04:55:12+00:00', '2026-03-07T07:23:17.998862+00:00', '{"Bust": "43 cm (flat)", "Length": "90 cm", "Waist": "35 cm (flat)", "Notes": "[Design Notes]Under waist: 42 cm (flat)", "Brand": "Haenuli", "Category": "JSK", "Features": ["Back Zip", "Dropped Waist", "No Shirring", "Pintucks"], "Colorways": "Purple", "Tags": "Pattern: Solid (OPJSK & SKs Only)"}')
ON CONFLICT(url) DO UPDATE SET
    name = excluded.name,
    brand = excluded.brand,
    category = excluded.category,
    published_at = excluded.published_at,
    scraped_at = excluded.scraped_at,
    extra_info = excluded.extra_info;

-- 插入图片
INSERT INTO lolibrary_images (item_id, image_url)
SELECT id, 'https://lolibrary.global.ssl.fastly.net/images/06co5PCm1tKDih4E8K4GsT7tcbRi0EFKndypVxWX.jpeg' FROM lolibrary_items WHERE url = 'https://lolibrary.org/items/haenuli-misty-violet-jsk';

-- 插入图片
INSERT INTO lolibrary_images (item_id, image_url)
SELECT id, 'https://lolibrary.global.ssl.fastly.net/images/x7xlZYcNY4izkj4jZvdmgztXa7pwfOvRnQSFS7aM.jpeg' FROM lolibrary_items WHERE url = 'https://lolibrary.org/items/haenuli-misty-violet-jsk';

-- 插入图片
INSERT INTO lolibrary_images (item_id, image_url)
SELECT id, 'https://lolibrary.global.ssl.fastly.net/images/3jgRQGk4QLCg8rtIUVLWY7rzr9VjU4OUSOBQqjLw.jpeg' FROM lolibrary_items WHERE url = 'https://lolibrary.org/items/haenuli-misty-violet-jsk';

-- 插入图片
INSERT INTO lolibrary_images (item_id, image_url)
SELECT id, 'https://lolibrary.global.ssl.fastly.net/images/1mcILJL5s1InRrT6Sbs0DjJrtufGL8GkKR6Yt5ET.jpeg' FROM lolibrary_items WHERE url = 'https://lolibrary.org/items/haenuli-misty-violet-jsk';

-- 插入图片
INSERT INTO lolibrary_images (item_id, image_url)
SELECT id, 'https://lolibrary.global.ssl.fastly.net/images/t73rKnDmEpVimd6RCVI1ZUvlCUEXnzVlKJF0U7gC.jpeg' FROM lolibrary_items WHERE url = 'https://lolibrary.org/items/haenuli-misty-violet-jsk';

-- 插入/更新商品: Sweet Picnic JSK...
INSERT INTO lolibrary_items (name, url, brand, category, published_at, scraped_at, extra_info) 
VALUES ('Sweet Picnic JSK', 'https://lolibrary.org/items/haenuli-sweet-picnic-jsk', 'Haenuli', 'JSK', '2026-03-07T04:43:28+00:00', '2026-03-07T07:23:19.801603+00:00', '{"Bust": "39-47 cm (flat)", "Length": "94 cm", "Waist": "33-44 cm (flat)", "Brand": "Haenuli", "Category": "JSK", "Features": ["Corset Lacing", "Partial Shirring", "Side Zip"], "Colorways": "Pink", "Tags": ["Cupcakes/Muffins", "Florals", "Food", "Strawberries"]}')
ON CONFLICT(url) DO UPDATE SET
    name = excluded.name,
    brand = excluded.brand,
    category = excluded.category,
    published_at = excluded.published_at,
    scraped_at = excluded.scraped_at,
    extra_info = excluded.extra_info;

-- 插入图片
INSERT INTO lolibrary_images (item_id, image_url)
SELECT id, 'https://lolibrary.global.ssl.fastly.net/images/KJ5WfWc5HTyMtDeJuIYMcyd9JqpwzlwVRqjm4s5d.jpeg' FROM lolibrary_items WHERE url = 'https://lolibrary.org/items/haenuli-sweet-picnic-jsk';

-- 插入图片
INSERT INTO lolibrary_images (item_id, image_url)
SELECT id, 'https://lolibrary.global.ssl.fastly.net/images/WmW4ga4DoLzIaKrry83FjtruEjQ3zB59pfVbeeiI.jpeg' FROM lolibrary_items WHERE url = 'https://lolibrary.org/items/haenuli-sweet-picnic-jsk';

-- 插入图片
INSERT INTO lolibrary_images (item_id, image_url)
SELECT id, 'https://lolibrary.global.ssl.fastly.net/images/795YKxYLCZPAcWzzcssUNmdO6srmzHXkY28jXjX7.jpeg' FROM lolibrary_items WHERE url = 'https://lolibrary.org/items/haenuli-sweet-picnic-jsk';

-- 插入图片
INSERT INTO lolibrary_images (item_id, image_url)
SELECT id, 'https://lolibrary.global.ssl.fastly.net/images/BOfCIe1jF2fg2pR4eNc6ChGZGXeOVvOfuDxJ8fN3.jpeg' FROM lolibrary_items WHERE url = 'https://lolibrary.org/items/haenuli-sweet-picnic-jsk';

-- 插入图片
INSERT INTO lolibrary_images (item_id, image_url)
SELECT id, 'https://lolibrary.global.ssl.fastly.net/images/ouoCZNHHgTKE5TLB8dQKz6M53yg2yGE0HJHl9nMa.jpeg' FROM lolibrary_items WHERE url = 'https://lolibrary.org/items/haenuli-sweet-picnic-jsk';

-- 插入/更新商品: Cherry Blossom JSKCherry Blossom...
INSERT INTO lolibrary_items (name, url, brand, category, published_at, scraped_at, extra_info) 
VALUES ('Cherry Blossom JSKCherry Blossom', 'https://lolibrary.org/items/haenuli-cherry-blossom-jsk', 'Haenuli', 'JSK', '2026-03-07T04:22:13+00:00', '2026-03-07T07:23:21.592976+00:00', '{"Brand": "Haenuli", "Category": "JSK", "Features": ["Corset Lacing", "Pintucks", "Scalloped", "Tiered Skirt"], "Colorways": "Wine/Bordeaux", "Tags": "Pattern: Solid (OPJSK & SKs Only)"}')
ON CONFLICT(url) DO UPDATE SET
    name = excluded.name,
    brand = excluded.brand,
    category = excluded.category,
    published_at = excluded.published_at,
    scraped_at = excluded.scraped_at,
    extra_info = excluded.extra_info;

-- 插入图片
INSERT INTO lolibrary_images (item_id, image_url)
SELECT id, 'https://lolibrary.global.ssl.fastly.net/images/QnRIHiXYDqP0rMp83986fdqb2iUPU55evWJ9xPDl.jpeg' FROM lolibrary_items WHERE url = 'https://lolibrary.org/items/haenuli-cherry-blossom-jsk';

-- 插入图片
INSERT INTO lolibrary_images (item_id, image_url)
SELECT id, 'https://lolibrary.global.ssl.fastly.net/images/oFVDFHWrZT6iGcty6zDOeObf0V5oYAXmmYAYfimd.jpeg' FROM lolibrary_items WHERE url = 'https://lolibrary.org/items/haenuli-cherry-blossom-jsk';

-- 插入/更新商品: A Hazy Picnic OP아련한 피크닉...
INSERT INTO lolibrary_items (name, url, brand, category, published_at, scraped_at, extra_info) 
VALUES ('A Hazy Picnic OP아련한 피크닉', 'https://lolibrary.org/items/haenuli-a-hazy-picnic-op', 'Haenuli', 'OP', '2026-03-07T04:16:18+00:00', '2026-03-07T07:23:23.354153+00:00', '{"Brand": "Haenuli", "Category": "OP", "Features": ["Peter Pan Collar", "Short Sleeves", "Tiered Skirt"], "Colorways": ["Blue", "Pink"], "Tags": ["Florals", "Pattern: PlaidsTartan"]}')
ON CONFLICT(url) DO UPDATE SET
    name = excluded.name,
    brand = excluded.brand,
    category = excluded.category,
    published_at = excluded.published_at,
    scraped_at = excluded.scraped_at,
    extra_info = excluded.extra_info;

-- 插入图片
INSERT INTO lolibrary_images (item_id, image_url)
SELECT id, 'https://lolibrary.global.ssl.fastly.net/images/GjtdGc2Nw2xu1iP67KZ0jMa4zguZFJjeFTczXafE.jpeg' FROM lolibrary_items WHERE url = 'https://lolibrary.org/items/haenuli-a-hazy-picnic-op';

-- 插入图片
INSERT INTO lolibrary_images (item_id, image_url)
SELECT id, 'https://lolibrary.global.ssl.fastly.net/images/g9ptg8tAIa6DQ2sDEUG6r4TaSagxb9Dj27ke5lO0.jpeg' FROM lolibrary_items WHERE url = 'https://lolibrary.org/items/haenuli-a-hazy-picnic-op';

-- 插入图片
INSERT INTO lolibrary_images (item_id, image_url)
SELECT id, 'https://lolibrary.global.ssl.fastly.net/images/wEvTaTHtWMhnnHQR7ppSOCwaoYDptoTRiwK9YLYn.jpeg' FROM lolibrary_items WHERE url = 'https://lolibrary.org/items/haenuli-a-hazy-picnic-op';

-- 插入/更新商品: Saint Lolita SkirtSaint LOLITA Skirt...
INSERT INTO lolibrary_items (name, url, brand, category, published_at, scraped_at, extra_info) 
VALUES ('Saint Lolita SkirtSaint LOLITA Skirt', 'https://lolibrary.org/items/haenuli-saint-lolita-skirt', 'Haenuli', 'Skirt', '2026-03-07T04:10:23+00:00', '2026-03-07T07:23:25.545207+00:00', '{"Brand": "Haenuli", "Category": "Skirt", "Features": "No features recorded!", "Colorways": "Black", "Tags": ["Angels/Cherubs", "Animals", "Roses"]}')
ON CONFLICT(url) DO UPDATE SET
    name = excluded.name,
    brand = excluded.brand,
    category = excluded.category,
    published_at = excluded.published_at,
    scraped_at = excluded.scraped_at,
    extra_info = excluded.extra_info;

-- 插入图片
INSERT INTO lolibrary_images (item_id, image_url)
SELECT id, 'https://lolibrary.global.ssl.fastly.net/images/JHU86PjonRQPslKeC2QElxuQ81RgvskzTs4DTrek.jpeg' FROM lolibrary_items WHERE url = 'https://lolibrary.org/items/haenuli-saint-lolita-skirt';