@echo off
echo ============================================
echo Installing dependencies with verbose output
echo ============================================

REM Try to run with admin privileges
powershell -Command "Start-Process cmd -ArgumentList '/c cd /d \"%~dp0\" && python -m pip install --verbose deep-translator textblob pyttsx3 customtkinter pillow mediapipe opencv-python numpy' -Verb RunAs"

echo.
echo If installation failed above, trying alternate installation method...
echo.

REM Direct pip install as fallback
python -m pip install --verbose deep-translator
python -m pip install --verbose textblob
python -m pip install --verbose pyttsx3
python -m pip install --verbose customtkinter
python -m pip install --verbose pillow
python -m pip install --verbose mediapipe
python -m pip install --verbose opencv-python
python -m pip install --verbose numpy

echo.
echo Testing if deep-translator was installed...
python -c "import deep_translator; print('SUCCESS: deep_translator is installed correctly!')" || echo "FAILED: deep_translator installation failed"

echo.
echo Dependencies installation completed.
echo Now you can run the simple_sign_detector.py directly.
echo.

pause 