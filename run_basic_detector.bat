@echo off
cd /d "%~dp0"
echo Running Basic Sign Language Detector...
echo This version has minimal dependencies and should work with basic opencv and mediapipe.
echo Press 'q' to quit.
echo.
python basic_sign_detector.py
pause 