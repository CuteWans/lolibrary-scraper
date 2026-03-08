import subprocess
import sys
import os

# 创建后台运行的VBScript - 使用原始字符串避免转义问题
vbscript_content = r'''Set WshShell = CreateObject("WScript.Shell")
WshShell.Run "python ""C:\Users\Administrator\clawd\skills\lolibrary-scraper\scripts\scraper.py"" --db-path ""C:\Users\Administrator\Documents\db\lolibrary.db"" --delay 0.1 --max-items 10000 --full-scrape", 0, False
Set WshShell = Nothing
'''

vbs_path = r'C:\Users\Administrator\clawd\skills\lolibrary-scraper\scripts\run_background.vbs'
with open(vbs_path, 'w', encoding='utf-8') as f:
    f.write(vbscript_content)

print(f"VBScript已创建: {vbs_path}")
print("\n使用方法:")
print("1. 双击运行 run_background.vbs 即可在后台启动")
print("2. 任务会在后台运行，关闭终端也不会停止")
print("3. 查看任务管理器中的 python.exe 进程确认运行状态")
