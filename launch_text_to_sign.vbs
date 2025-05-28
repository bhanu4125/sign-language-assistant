Set WshShell = CreateObject("WScript.Shell")
WshShell.CurrentDirectory = "C:\Users\tumma\OneDrive\Documents\text to sign"
WshShell.Run "python main.py", 1, False 