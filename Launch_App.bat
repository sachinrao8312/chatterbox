@echo off
title Chatterbox AI
cd /d "%~dp0"

echo.
echo  ========================================
echo    Chatterbox AI Dashboard
echo  ========================================
echo.

REM Use virtual environment if available
if exist ".venv\Scripts\python.exe" (
    .venv\Scripts\python.exe desktop_app.py
) else (
    python desktop_app.py
)
