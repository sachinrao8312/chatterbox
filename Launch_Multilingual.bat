@echo off
title Chatterbox TTS - Multilingual Mode
cd /d "%~dp0"

echo.
echo  ========================================
echo    Chatterbox TTS - Multilingual Mode
echo    (23+ Languages)
echo  ========================================
echo.

REM Use virtual environment if available
if exist ".venv\Scripts\python.exe" (
    .venv\Scripts\python.exe desktop_app.py multilingual
) else (
    python desktop_app.py multilingual
)
