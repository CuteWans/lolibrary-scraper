#!/usr/bin/env python3
"""
Lolibrary 抓取任务监控脚本
定时检查抓取任务状态，如果任务中断则自动重启
"""

import subprocess
import sys
import time
import json
from pathlib import Path
from datetime import datetime, timedelta

# 配置
SCRAPER_SCRIPT = Path(__file__).parent / "scraper.py"
STATE_FILE = Path(__file__).parent.parent / "output" / "scraper_state.json"
DB_PATH = r"C:\Users\Administrator\Documents\db\lolibrary.db"
IMAGE_DIR = r"C:\Users\Administrator\Pictures\lolibrary"
LOG_FILE = Path(__file__).parent.parent / "output" / "monitor.log"
CHECK_INTERVAL = 300  # 每5分钟检查一次
TIMEOUT_SECONDS = 600  # 10分钟无更新认为任务卡住


def log(message: str):
    """记录日志"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_msg = f"[{timestamp}] {message}"
    print(log_msg)
    
    # 写入日志文件
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(log_msg + '\n')


def get_state():
    """获取当前抓取状态"""
    if not STATE_FILE.exists():
        return None
    
    try:
        with open(STATE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        log(f"读取状态文件失败: {e}")
        return None


def is_scraper_running():
    """检查抓取进程是否在运行"""
    try:
        # Windows: 使用 tasklist 检查 python 进程
        result = subprocess.run(
            ['tasklist', '/FI', 'IMAGENAME eq python.exe', '/FO', 'CSV'],
            capture_output=True,
            text=True
        )
        
        # 检查输出中是否包含 scraper.py
        if 'scraper.py' in result.stdout:
            return True
        
        # 备选：检查是否有 python 进程在运行（可能不准确）
        return 'python.exe' in result.stdout and result.stdout.count('python.exe') > 1
    
    except Exception as e:
        log(f"检查进程失败: {e}")
        return False


def start_scraper():
    """启动抓取任务"""
    log("启动抓取任务...")
    
    try:
        # 使用 Popen 启动后台进程
        process = subprocess.Popen(
            [
                sys.executable,
                str(SCRAPER_SCRIPT),
                '--db-path', DB_PATH,
                '--image-dir', IMAGE_DIR,
                '--delay', '0.1',
                '--full-scrape'
            ],
            cwd=str(SCRAPER_SCRIPT.parent),
            creationflags=subprocess.CREATE_NEW_CONSOLE  # Windows: 创建新控制台窗口
        )
        
        log(f"抓取任务已启动，PID: {process.pid}")
        return process.pid
    
    except Exception as e:
        log(f"启动抓取任务失败: {e}")
        return None


def check_and_restart():
    """检查任务状态并在需要时重启"""
    state = get_state()
    
    if state:
        log(f"当前状态 - 页码: {state.get('current_page', 1)}, 已抓取: {state.get('total_items_scraped', 0)} 个商品")
        
        # 检查上次更新时间
        last_run = state.get('last_run')
        if last_run:
            try:
                from datetime import datetime
                last_time = datetime.fromisoformat(last_run)
                elapsed = (datetime.now() - last_time).total_seconds()
                
                if elapsed > TIMEOUT_SECONDS:
                    log(f"警告: 任务已 {elapsed/60:.1f} 分钟无更新")
            except:
                pass
    
    # 检查进程是否在运行
    if not is_scraper_running():
        log("抓取任务未运行，准备重启...")
        pid = start_scraper()
        if pid:
            log(f"抓取任务已重启，PID: {pid}")
        else:
            log("重启失败")
    else:
        log("抓取任务正在运行中")


def main():
    """主函数 - 持续监控"""
    log("=" * 60)
    log("Lolibrary 抓取任务监控启动")
    log(f"检查间隔: {CHECK_INTERVAL} 秒")
    log(f"超时时间: {TIMEOUT_SECONDS} 秒")
    log("=" * 60)
    
    # 立即检查一次
    check_and_restart()
    
    # 定时检查
    while True:
        time.sleep(CHECK_INTERVAL)
        check_and_restart()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        log("监控脚本已停止")
        sys.exit(0)
