import sys
import os
import traceback
import io

# 设置输出编码
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# 添加脚本目录到路径
sys.path.insert(0, r'C:\Users\Administrator\clawd\skills\lolibrary-scraper\scripts')

print("开始运行...")
print(f"Python版本: {sys.version}")

try:
    from scraper import LolibraryScraper
    
    scraper = LolibraryScraper(
        delay=0.1, 
        db_path=r'C:\Users\Administrator\Documents\db\lolibrary.db'
    )
    scraper.last_scrape_time = None
    print("完整抓取模式")
    print(f"从第 {scraper.current_page} 页开始")
    
    result = scraper.scrape(max_items=1000)
    print(f"完成！共抓取 {result} 个商品")
    
    scraper.finish()
    print("正常结束")
    
except Exception as e:
    print(f"\n\n===== 发生错误 =====")
    print(f"错误类型: {type(e).__name__}")
    print(f"错误信息: {e}")
    print(f"\n详细错误堆栈:")
    traceback.print_exc()
    
    # 尝试保存状态
    try:
        if 'scraper' in dir():
            scraper._save_state()
            print("\n状态已保存")
    except Exception as save_error:
        print(f"保存状态失败: {save_error}")
    
    sys.exit(1)
