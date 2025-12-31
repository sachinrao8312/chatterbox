"""
Create Desktop Shortcuts for Chatterbox TTS
Run this script to create desktop shortcuts for all TTS modes.
"""

import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DESKTOP = os.path.join(os.path.expanduser("~"), "Desktop")


def find_python():
    """Find Python executable, prefer venv"""
    venv_python = os.path.join(SCRIPT_DIR, ".venv", "Scripts", "pythonw.exe")
    if os.path.exists(venv_python):
        return venv_python
    pythonw = sys.executable.replace("python.exe", "pythonw.exe")
    if os.path.exists(pythonw):
        return pythonw
    return sys.executable


def create_vbs_shortcut(name, mode):
    """Create a VBS launcher script on desktop"""
    python_exe = find_python()
    app_script = os.path.join(SCRIPT_DIR, "desktop_app.py")
    vbs_path = os.path.join(DESKTOP, f"{name}.vbs")
    
    vbs_content = f'''Set WshShell = CreateObject("WScript.Shell")
WshShell.CurrentDirectory = "{SCRIPT_DIR}"
WshShell.Run """{python_exe}"" ""{app_script}"" {mode}", 0, False
'''
    
    try:
        with open(vbs_path, 'w') as f:
            f.write(vbs_content)
        return True
    except Exception as e:
        print(f"   ❌ Failed: {e}")
        return False


def main():
    print()
    print("=" * 55)
    print("  🎙️ Chatterbox TTS - Desktop Shortcut Creator")
    print("=" * 55)
    print()
    
    shortcuts = [
        ("Chatterbox TTS (Turbo)", "turbo"),
        ("Chatterbox TTS (Standard)", "standard"),
        ("Chatterbox TTS (Multilingual)", "multilingual"),
    ]
    
    created = 0
    
    for name, mode in shortcuts:
        print(f"  Creating: {name}...", end=" ")
        if create_vbs_shortcut(name, mode):
            print("✅")
            created += 1
        else:
            print("❌")
    
    print()
    print("-" * 55)
    print(f"  ✨ Created {created}/{len(shortcuts)} shortcuts on Desktop!")
    print()
    print("  📁 Shortcuts created:")
    for name, mode in shortcuts:
        print(f"     • {name}")
    print()
    print("  💡 Double-click any shortcut to launch that mode!")
    print("=" * 55)
    print()


if __name__ == "__main__":
    main()
