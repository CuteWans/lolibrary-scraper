Set WshShell = CreateObject("WScript.Shell")
WshShell.Run "python ""C:\Users\Administrator\clawd\skills\lolibrary-scraper\scripts\scraper.py"" --db-path ""C:\Users\Administrator\Documents\db\lolibrary.db"" --delay 0.1 --full-scrape", 0, False
Set WshShell = Nothing
