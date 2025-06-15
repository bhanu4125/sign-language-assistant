@echo off
cd /d "%~dp0"
start "Sign to Text" cmd /k "python inference_classifier.py" 