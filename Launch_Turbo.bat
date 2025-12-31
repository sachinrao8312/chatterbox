@echo off
title Chatterbox TTS - Turbo Mode
cd /d "%~dp0"

echo.
echo  ========================================
echo    Chatterbox TTS - Turbo Mode
echo  ========================================
echo.

REM Use virtual environment if available
if exist ".venv\Scripts\python.exe" (
    .venv\Scripts\python.exe desktop_app.py turbo
) else (
    python desktop_app.py turbo
)
