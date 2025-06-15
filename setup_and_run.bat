@echo off
cd /d "%~dp0"
echo Sign Language Detection System Setup

echo Installing required dependencies...
python -m pip install deep-translator textblob pyttsx3 customtkinter pillow mediapipe opencv-python numpy

echo.
echo Would you like to run a system test first to check if everything is working? (Y/N)
set /p choice=
if /i "%choice%"=="Y" (
    echo.
    echo Running system test...
    python camera_test.py
    echo.
    echo Test completed.
)

echo.
echo Starting Sign Language Detector...
python inference_classifier.py 