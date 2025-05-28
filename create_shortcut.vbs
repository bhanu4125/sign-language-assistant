Set objShell = CreateObject("WScript.Shell")
strDesktop = objShell.SpecialFolders("Desktop")

Set objShortcut = objShell.CreateShortcut(strDesktop & "\Sign Language Assistant.lnk")
objShortcut.TargetPath = "C:\Users\tumma\OneDrive\Documents\2nd chance\dti 2\launcher.html"
objShortcut.Description = "Launch Sign Language Applications"
objShortcut.IconLocation = "C:\Windows\System32\shell32.dll,44"
objShortcut.Save 