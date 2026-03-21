Set objShell = CreateObject("WScript.Shell")
objShell.CurrentDirectory = "C:\Users\Administrator\clawd\skills\lolibrary-scraper"
objShell.Run "python scripts/scraper.py --db-path ""C:\Users\Administrator\Documents\db\lolibrary.db"" --delay 0.05", 0, False
