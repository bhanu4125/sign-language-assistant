@echo off
cd /d "%~dp0"
echo Installing required packages...
python -m pip install opencv-python mediapipe numpy

echo.
echo Starting minimal sign language detector...
echo This is a simplified version that should work reliably.
echo.
python minimal_detector.py
pause 