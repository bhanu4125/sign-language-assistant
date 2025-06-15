@echo off
cd /d "%~dp0"
echo Running Simplified Sign Language Detector...
echo This version has minimal dependencies and should work if the full version doesn't.
echo Press 'q' to quit.
echo.
python simple_sign_detector.py
pause 