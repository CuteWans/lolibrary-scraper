import subprocess
import sys

# 运行脚本并捕获输出
process = subprocess.Popen(
    [sys.executable, 'scripts/scraper.py', '--db-path', r'C:\Users\Administrator\Documents\db\lolibrary.db', '--delay', '0.1', '--max-items', '1000', '--full-scrape'],
    cwd=r'C:\Users\Administrator\clawd\skills\lolibrary-scraper',
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True,
    encoding='utf-8',
    errors='replace'
)

# 实时输出
for line in process.stdout:
    print(line, end='')

process.wait()
print(f"\n\n进程退出，返回码: {process.returncode}")
