@echo off
echo Starting Sign Language Web Application...

REM Activate virtual environment if it exists
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
) else (
    echo Virtual environment not found. Please run setup first.
    exit /b 1
)

REM Check if model file exists
if not exist "model.p" (
    echo Error: model.p file not found!
    echo Please ensure the model file is in the same directory as this script.
    exit /b 1
)

REM Create logs directory if it doesn't exist
if not exist "logs" mkdir logs

REM Start the server
echo Starting server...
python waitress_server.py

pause 