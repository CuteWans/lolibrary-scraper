#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""测试运行脚本 - 直接输出错误"""

import sys
import traceback

try:
    from scripts.scraper import LolibraryScraper
    
    print("创建抓取器...")
    scraper = LolibraryScraper(delay=0.05, db_path=r"C:/Users/Administrator/Documents/db/lolibrary.db")
    
    print(f"last_scrape_time: {scraper.last_scrape_time}")
    print(f"current_page: {scraper.current_page}")
    
    print("设置为全量模式...")
    scraper.last_scrape_time = None
    
    print("开始抓取（不限制数量，连续 3 页无数据停止）...")
    result = scraper.scrape(max_items=None)
    
    print(f"完成！新增：{result}")
    scraper.finish()
    
except Exception as e:
    print(f"\n❌ 错误：{e}")
    traceback.print_exc()
    sys.exit(1)
