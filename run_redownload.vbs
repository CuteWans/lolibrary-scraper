Set objShell = CreateObject("WScript.Shell")
objShell.CurrentDirectory = "C:\Users\Administrator\clawd\skills\lolibrary-scraper"
objShell.Run "python scripts/redownload_missing.py --auto", 0, False
