
import os
import sys
import subprocess
from PIL import Image

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DESKTOP = os.path.join(os.path.expanduser("~"), "Desktop")
ICON_PNG = os.path.join(SCRIPT_DIR, "app_icon.png")
ICON_ICO = os.path.join(SCRIPT_DIR, "app_icon.ico")
APP_SCRIPT = "desktop_app.py"

def find_pythonw():
    """Find PythonW executable in venv"""
    venv_pythonw = os.path.join(SCRIPT_DIR, ".venv", "Scripts", "pythonw.exe")
    if os.path.exists(venv_pythonw):
        return venv_pythonw
    return sys.executable.replace("python.exe", "pythonw.exe")

def convert_icon():
    """Convert PNG to ICO"""
    if not os.path.exists(ICON_PNG):
        print(f"❌ Source icon not found: {ICON_PNG}")
        return False
        
    try:
        img = Image.open(ICON_PNG)
        # Create sizes for the icon
        img.save(ICON_ICO, format='ICO', sizes=[(256, 256)])
        print(f"✅ Created icon: {ICON_ICO}")
        return True
    except Exception as e:
        print(f"❌ Failed to convert icon: {e}")
        return False

def create_shortcut_ps(name):
    """Create a .lnk shortcut using PowerShell"""
    pythonw = find_pythonw()
    shortcut_path = os.path.join(DESKTOP, f"{name}.lnk")
    
    # PowerShell script to create shortcut
    # Note: quoted paths to handle spaces
    ps_script = f"""
    $WshShell = New-Object -comObject WScript.Shell
    $Shortcut = $WshShell.CreateShortcut("{shortcut_path}")
    $Shortcut.TargetPath = "{pythonw}"
    $Shortcut.Arguments = "{APP_SCRIPT}"
    $Shortcut.WorkingDirectory = "{SCRIPT_DIR}"
    $Shortcut.IconLocation = "{ICON_ICO}"
    $Shortcut.Save()
    """
    
    try:
        cmd = ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", ps_script]
        subprocess.run(cmd, check=True, capture_output=True, text=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ PowerShell failed: {e.stderr}")
        return False
    except Exception as e:
        print(f"❌ Failed to create shortcut: {e}")
        return False

def main():
    print("=" * 50)
    print(" 🎨 Chatterbox Shortcut Creator")
    print("=" * 50)
    
    # 1. Convert Icon
    if not convert_icon():
        return
        
    # 2. Create Shortcut
    name = "Chatterbox AI"
    print(f"Creating shortcut '{name}' on Desktop...")
    
    if create_shortcut_ps(name):
        print(f"✅ Success! Shortcut created on Desktop.")
        print(f"   Target: {find_pythonw()}")
        print(f"   Icon:   {ICON_ICO}")
    else:
        print("❌ Failed to create shortcut.")

if __name__ == "__main__":
    main()
