@echo off
cd /d "%~dp0"
echo =====================================
echo Running Standalone Sign-to-Text Detector
echo =====================================
echo This is a standalone version with minimal dependencies
echo that should work with just opencv and mediapipe installed.
echo.
echo Installing core dependencies if needed...
python -m pip install opencv-python mediapipe numpy
echo.
echo Starting detector...
echo Press 'q' to quit, 'c' to clear text
echo.
python standalone_detector.py
pause 