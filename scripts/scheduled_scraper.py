#!/usr/bin/env python3
"""
Lolibrary.org 定时抓取任务调度脚本
每周三和周日执行增量抓取任务
"""

import subprocess
import sys
import os
from datetime import datetime
from pathlib import Path

# 配置
SCRAPER_SCRIPT = Path(__file__).parent / "scraper.py"
OUTPUT_DIR = Path(__file__).parent.parent / "output"
LOG_FILE = OUTPUT_DIR / "scraper.log"

# 确保输出目录存在
OUTPUT_DIR.mkdir(exist_ok=True)


def run_scraper():
    """执行增量抓取任务"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    json_file = OUTPUT_DIR / f"lolibrary_data_{timestamp}.json"
    sql_file = OUTPUT_DIR / f"lolibrary_data_{timestamp}.sql"
    state_file = OUTPUT_DIR / "scraper_state.json"
    
    print(f"[{datetime.now()}] 开始执行增量抓取任务...")
    
    cmd = [
        sys.executable,
        str(SCRAPER_SCRIPT),
        "--output-json", str(json_file),
        "--output-sql", str(sql_file),
        "--state-file", str(state_file),
        "--delay", "1.0"
    ]
    
    try:
        # 执行抓取脚本
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True
        )
        
        # 记录日志
        with open(LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(f"\n{'='*60}\n")
            f.write(f"[{datetime.now()}] 增量抓取任务执行成功\n")
            f.write(f"stdout:\n{result.stdout}\n")
            if result.stderr:
                f.write(f"stderr:\n{result.stderr}\n")
        
        print(f"[{datetime.now()}] 抓取任务完成")
        print(f"JSON输出: {json_file}")
        print(f"SQL输出: {sql_file}")
        
        return True
        
    except subprocess.CalledProcessError as e:
        # 记录错误日志
        with open(LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(f"\n{'='*60}\n")
            f.write(f"[{datetime.now()}] 抓取任务执行失败\n")
            f.write(f"Return code: {e.returncode}\n")
            f.write(f"stdout:\n{e.stdout}\n")
            f.write(f"stderr:\n{e.stderr}\n")
        
        print(f"[{datetime.now()}] 抓取任务失败，详见日志: {LOG_FILE}")
        return False


def should_run_today():
    """检查今天是否应该运行（周三或周日）"""
    today = datetime.now().weekday()
    # 周一=0, 周三=2, 周日=6
    return today in [2, 6]  # 周三或周日


def main():
    """主函数"""
    # 检查今天是否应该运行
    if not should_run_today():
        print(f"[{datetime.now()}] 今天不是抓取日（仅在周三和周日运行）")
        return 0
    
    # 执行抓取
    success = run_scraper()
    return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main())
