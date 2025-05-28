Set WshShell = CreateObject("WScript.Shell")
WshShell.CurrentDirectory = "C:\Users\tumma\OneDrive\Documents\2nd chance\dti 2"
WshShell.Run "python inference_classifier.py", 1, False 