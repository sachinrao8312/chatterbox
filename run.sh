#!/bin/bash

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

echo "========================================"
echo "  Chatterbox AI Dashboard"
echo "========================================"
echo ""

# Use virtual environment if available (checking for Windows path layout in Git Bash)
if [ -f ".venv/Scripts/python.exe" ]; then
    ./.venv/Scripts/python.exe desktop_app.py "$@"
elif [ -f ".venv/bin/python" ]; then
    ./.venv/bin/python desktop_app.py "$@"
else
    python desktop_app.py "$@"
fi
