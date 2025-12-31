@echo off
title Chatterbox TTS - Standard Mode
cd /d "%~dp0"

echo.
echo  ========================================
echo    Chatterbox TTS - Standard Mode
echo  ========================================
echo.

REM Use virtual environment if available
if exist ".venv\Scripts\python.exe" (
    .venv\Scripts\python.exe desktop_app.py standard
) else (
    python desktop_app.py standard
)
