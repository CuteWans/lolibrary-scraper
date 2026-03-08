import sys
import os
import traceback

# 添加脚本目录到路径
sys.path.insert(0, r'C:\Users\Administrator\clawd\skills\lolibrary-scraper\scripts')

# 导入并运行
from scraper import LolibraryScraper

print("开始运行...")
try:
    scraper = LolibraryScraper(
        delay=0.1, 
        db_path=r'C:\Users\Administrator\Documents\db\lolibrary.db'
    )
    scraper.last_scrape_time = None
    print("完整抓取模式")
    
    result = scraper.scrape(max_items=1000)
    print(f"完成！共抓取 {result} 个商品")
    
    scraper.finish()
except Exception as e:
    print(f"\n\n发生错误: {e}")
    print("\n详细错误信息:")
    traceback.print_exc()
    
    # 保存状态
    try:
        scraper._save_state()
        print("\n状态已保存")
    except:
        pass
