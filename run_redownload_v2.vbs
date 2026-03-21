Set objShell = CreateObject("WScript.Shell")
objShell.CurrentDirectory = "C:\Users\Administrator\clawd\skills\lolibrary-scraper"
objShell.Run "python scripts/redownload_missing_v2.py", 0, False
