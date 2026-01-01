"""
Chatterbox TTS - Desktop Application
A native desktop app that runs the Gradio TTS server and displays it in a native window.
Can be run in "Dashboard" mode to switch between models, or directly with a specific mode.
"""

import webview
import webbrowser
import threading
import subprocess
import sys
import os
import time
import socket
import webview
import webbrowser
import threading
import subprocess
import sys
import os
import time
import socket
import atexit
import json

# Configuration
APP_TITLE = "Chatterbox TTS"
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_PORT = 7860
SETTINGS_FILE = os.path.join(SCRIPT_DIR, "settings.json")

# Global state
server_process = None
server_url = None
main_window = None

def load_settings():
    try:
        if os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE, 'r') as f:
                return json.load(f)
    except:
        pass
    return {"output_dir": os.path.join(os.path.expanduser("~"), "Music", "Chatterbox Output")}

def save_settings(settings):
    try:
        with open(SETTINGS_FILE, 'w') as f:
            json.dump(settings, f, indent=4)
    except:
        pass

# HTML Templates
DASHBOARD_HTML = """
<!DOCTYPE html>
<html>
<head>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            color: white;
            padding: 40px;
        }
        
        .header {
            text-align: center;
            margin-bottom: 60px;
            animation: fadeIn 1s ease;
        }
        
        .logo {
            font-size: 64px;
            margin-bottom: 10px;
            display: inline-block;
            animation: float 3s ease-in-out infinite;
        }
        
        h1 {
            font-size: 42px;
            font-weight: 700;
            margin-bottom: 10px;
            background: linear-gradient(90deg, #00d4ff, #00ff88);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .subtitle {
            font-size: 18px;
            color: #a0a0c0;
        }
        
        .grid {

            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 30px;
            max-width: 1200px;
            width: 100%;
            animation: slideUp 0.8s ease;
        }
        
        .card {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 20px;
            padding: 30px;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
            backdrop-filter: blur(10px);
        }
        
        .card:hover {
            transform: translateY(-10px);
            background: rgba(255, 255, 255, 0.1);
            border-color: rgba(0, 212, 255, 0.3);
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
        }
        
        .card-icon {
            font-size: 48px;
            margin-bottom: 20px;
        }
        
        .card h2 {
            font-size: 24px;
            margin-bottom: 10px;
            color: #fff;
        }
        
        .card p {
            color: #a0a0c0;
            font-size: 14px;
            line-height: 1.6;
            margin-bottom: 20px;
        }
        
        .btn {
            background: linear-gradient(90deg, #00d4ff, #00b8d4);
            color: #1a1a2e;
            padding: 10px 24px;
            border-radius: 50px;
            font-weight: 600;
            border: none;
            cursor: pointer;
            transition: transform 0.2s;
            display: inline-block;
        }
        
        .card:hover .btn {
            transform: scale(1.05);
            box-shadow: 0 0 20px rgba(0, 212, 255, 0.4);
        }

        .settings-btn {
            position: absolute;
            top: 20px;
            right: 20px;
            background: rgba(255, 255, 255, 0.1);
            border: none;
            color: #a0a0c0;
            padding: 10px;
            border-radius: 50%;
            cursor: pointer;
            transition: all 0.2s;
            font-size: 20px;
            width: 44px;
            height: 44px;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .settings-btn:hover {
            background: rgba(255, 255, 255, 0.2);
            color: white;
            transform: rotate(45deg);
        }

        /* Modal */
        .modal-overlay {
            display: none;
            position: fixed;
            top: 0; left: 0; right: 0; bottom: 0;
            background: rgba(0,0,0,0.7);
            z-index: 1000;
            backdrop-filter: blur(5px);
            align-items: center;
            justify-content: center;
        }
        
        .modal {
            background: #16213e;
            padding: 30px;
            border-radius: 20px;
            width: 500px;
            border: 1px solid rgba(255,255,255,0.1);
            box-shadow: 0 20px 40px rgba(0,0,0,0.5);
            animation: slideUp 0.4s ease;
        }
        
        .modal h2 {
            margin-bottom: 20px;
            color: #fff;
            border-bottom: 1px solid rgba(255,255,255,0.1);
            padding-bottom: 15px;
        }
        
        .input-group {
            margin-bottom: 20px;
        }
        
        .input-group label {
            display: block;
            color: #a0a0c0;
            margin-bottom: 8px;
            font-size: 14px;
        }
        
        .folder-picker {
            display: flex;
            gap: 10px;
        }
        
        .folder-input {
            flex: 1;
            background: rgba(0,0,0,0.2);
            border: 1px solid rgba(255,255,255,0.1);
            padding: 10px;
            border-radius: 8px;
            color: #fff;
            font-family: monospace;
        }
        
        .btn-small {
            background: rgba(0, 212, 255, 0.1);
            color: #00d4ff;
            border: 1px solid rgba(0, 212, 255, 0.3);
            border-radius: 8px;
            padding: 0 15px;
            cursor: pointer;
            font-weight: 600;
        }
        
        .btn-save {
            background: #00d4ff;
            color: #1a1a2e;
            width: 100%;
            padding: 12px;
            border: none;
            border-radius: 8px;
            font-weight: 700;
            cursor: pointer;
            margin-top: 10px;
        }

        .turbo-accent { color: #ffe600; }
        .std-accent { color: #00d4ff; }
        .multi-accent { color: #ff007f; }

        @keyframes float {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-10px); }
        }
        
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        
        @keyframes slideUp {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
    </style>
</head>
<body>

    <button class="settings-btn" onclick="openSettings()" title="Settings" style="right: 70px;">⚙️</button>
    <button class="settings-btn" onclick="quitApp()" title="Quit" style="right: 20px; color: #ff4d4d;">❌</button>

    <div class="header">
        <div class="logo">🎙️</div>
        <h1>Chatterbox TTS</h1>
        <p class="subtitle">Select a mode to launch the AI workspace</p>
    </div>
    
    <div class="grid">
        <div class="card" onclick="launch('turbo')">
            <div class="card-icon">⚡</div>
            <h2 class="turbo-accent">Turbo Mode</h2>
            <p>Optimized for speed and low latency. Best for quick generations and real-time experimentation.</p>
            <button class="btn">Launch Turbo</button>
        </div>
        
        <div class="card" onclick="launch('standard')">
            <div class="card-icon">✨</div>
            <h2 class="std-accent">Standard Mode</h2>
            <p>High-fidelity audio generation. The balanced choice for quality and performance.</p>
            <button class="btn">Launch Standard</button>
        </div>
        
        <div class="card" onclick="launch('multilingual')">
            <div class="card-icon">🌍</div>
            <h2 class="multi-accent">Multilingual</h2>
            <p>Support for 23+ languages including French, German, Spanish, and many more.</p>

            <button class="btn">Launch Multi</button>
        </div>

        <div class="card" onclick="launch('voice_conversion')">
            <div class="card-icon">🎭</div>
            <h2 style="color: #a29bfe;">Voice Conversion</h2>
            <p>Clone and convert voices using reference audio. Transfer timbre and style effectively.</p>
            <button class="btn">Launch VC</button>
        </div>
    </div>

    <!-- Settings Modal -->
    <div class="modal-overlay" id="settingsModal">
        <div class="modal">
            <h2>⚙️ Settings</h2>
            
            <div class="input-group">
                <label>Output Directory (Where audio is saved)</label>
                <div class="folder-picker">
                    <input type="text" id="outputDir" class="folder-input" readonly>
                    <button class="btn-small" onclick="browseFolder()">📂 Browse</button>
                </div>
            </div>
            
            <button class="btn-save" onclick="saveAndClose()">Save Settings</button>
            <button class="btn-save" style="background:transparent; color:#888; margin-top:0;" onclick="closeSettings()">Cancel</button>
        </div>
    </div>

    <script>
        function launch(mode) {
            const cards = document.querySelectorAll('.card');
            cards.forEach(c => c.style.opacity = '0.5');
            // Fire and forget - do NOT await this, as the page will unload
            pywebview.api.launch_mode(mode).catch(() => {});
        }

        async function openSettings() {
            // Get current settings from Python
            const settings = await pywebview.api.get_settings();
            document.getElementById('outputDir').value = settings.output_dir || "";
            
            document.getElementById('settingsModal').style.display = 'flex';
        }

        function closeSettings() {
            document.getElementById('settingsModal').style.display = 'none';
        }

        async function browseFolder() {
            const path = await pywebview.api.choose_folder();
            if (path) {
                document.getElementById('outputDir').value = path;
            }
        }

        async function saveAndClose() {
            const dir = document.getElementById('outputDir').value;
            await pywebview.api.save_settings({ output_dir: dir });
            closeSettings();
        }
        

        async function quitApp() {
            if(confirm("Are you sure you want to quit?")) {
                await pywebview.api.quit_app();
            }
        }

        // Close on clean click outside
        document.getElementById('settingsModal').addEventListener('click', function(e) {
            if (e.target === this) closeSettings();
        });
    </script>
</body>
</html>
"""

LOADING_HTML = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body {
            font-family: 'Segoe UI', sans-serif;
            background: #1a1a2e;
            color: white;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            flex-direction: column;
        }
        .loader {
            width: 50px;
            height: 50px;
            border: 3px solid rgba(255,255,255,0.1);
            border-top-color: #00d4ff;
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin-bottom: 20px;
        }
        @keyframes spin { to { transform: rotate(360deg); } }
        h2 { font-weight: 300; color: #00d4ff; }
        p { color: #888; font-size: 14px; }
    </style>
</head>
<body>
    <div class="loader"></div>
    <h2 id="status">Starting Engine...</h2>
    <p>Please wait while we load the AI models.</p>
</body>
</html>
"""


# HTML for the injected Home/Settings buttons
INJECT_BUTTONS_OPTS = """
(function() {
    if (document.getElementById('chatterbox-controls')) return;
    
    const container = document.createElement('div');
    container.id = "chatterbox-controls";
    container.style.cssText = "position: fixed; top: 10px; right: 10px; z-index: 99999; display: flex; gap: 10px;";
    
    // Home Button
    const homeBtn = document.createElement('button');
    homeBtn.innerHTML = "🏠 Home";
    homeBtn.style.cssText = "background: #16213e; color: #00d4ff; border: 1px solid rgba(0, 212, 255, 0.3); padding: 8px 16px; border-radius: 20px; cursor: pointer; font-family: sans-serif; font-weight: bold; box-shadow: 0 4px 6px rgba(0,0,0,0.3);";
    homeBtn.onclick = function() { window.pywebview.api.go_home(); };
    homeBtn.onmouseover = function() { this.style.background = "#1a1a2e"; };
    homeBtn.onmouseout = function() { this.style.background = "#16213e"; };
    
    // Quit Button
    const quitBtn = document.createElement('button');
    quitBtn.innerHTML = "❌ Quit";
    quitBtn.style.cssText = "background: #3e1616; color: #ff4d4d; border: 1px solid rgba(255, 77, 77, 0.3); padding: 8px 16px; border-radius: 20px; cursor: pointer; font-family: sans-serif; font-weight: bold; box-shadow: 0 4px 6px rgba(0,0,0,0.3);";
    quitBtn.onclick = function() { window.pywebview.api.quit_app(); };
    quitBtn.onmouseover = function() { this.style.background = "#2d1010"; };
    quitBtn.onmouseout = function() { this.style.background = "#3e1616"; };

    container.appendChild(homeBtn);
    container.appendChild(quitBtn);
    document.body.appendChild(container);
})();
"""

class Api:
    """JavaScript API for the webview"""
    
    def launch_mode(self, mode):
        """Called from Dashboard to launch a specific mode"""
        print(f"[API] Request to launch: {mode}")
        # We start the switch in a thread and return immediately.
        # Impt: JS should NOT await this call, or if it does, it will complete 'undefined'
        # before the page unloads.
        threading.Thread(target=self._switch_mode, args=(mode,), daemon=True).start()
        return "OK"
    
    def _switch_mode(self, mode):
        """Internal method to handle the switching logic"""
        global main_window
        
        # Give a short delay to allow the `launch_mode` return value ("OK") to reach the frontend 
        # API callback BEFORE we destroy the page context with load_html.
        time.sleep(0.5)
        
        # 1. Show loading screen (HTML content is fine here as it doesn't access network)
        if main_window:
            main_window.load_html(LOADING_HTML)
        
        # 2. Stop existing server
        stop_gradio_server()
        
        # 3. Start new server
        url = start_gradio_server(mode)
        
        if url and main_window:
            # Short delay to allow any pending API returns (like launch_mode) to flush to the old JS context
            # before we nuke it with load_url
            time.sleep(0.5)
            
            # Navigate the main window to the localhost URL
            # This avoids "Public page connecting to local network" errors
            main_window.load_url(url)
            
            # 5. Inject the Home button after a short delay to ensure page load
            # Note: In a robust app we might poll, but a delay is usually sufficient for local server
            time.sleep(1) 
            main_window.evaluate_js(INJECT_BUTTONS_OPTS)
            
            # Keep re-injecting periodically in case the user navigates within Gradio
            # or if the page took longer to load
            for _ in range(5):
                time.sleep(1)
                main_window.evaluate_js(INJECT_BUTTONS_OPTS)
                
        elif main_window:
             main_window.load_html("<h1>Error starting server. Check console.</h1>")

    def go_home(self):
        """Return to dashboard"""
        print("[API] Returning to home")
        threading.Thread(target=self._go_home_thread, daemon=True).start()
        
    def _go_home_thread(self):
        global main_window
        # Stop server to free up resources/ports
        stop_gradio_server()
        if main_window:
            main_window.load_html(DASHBOARD_HTML)

    def open_in_browser(self):
        """Open current server URL in system browser"""
        if server_url:
            webbrowser.open(server_url)

    def get_settings(self):
        return load_settings()

    def save_settings(self, settings):
        # Fix: call the global save_settings function, not self.save_settings (recursion)
        try:
            with open(SETTINGS_FILE, 'w') as f:
                json.dump(settings, f, indent=4)
        except Exception as e:
            print(f"Error saving settings: {e}")
        return True


    def quit_app(self):
        """Quit the application"""
        print("[API] Quitting application")
        global main_window
        if main_window:
            main_window.destroy()
        
        # Ensure server is stopped
        stop_gradio_server()
        sys.exit(0)

    def choose_folder(self):
        global main_window
        if main_window:
            result = main_window.create_file_dialog(webview.FOLDER_DIALOG)
            if result and len(result) > 0:
                return result[0]
        return None


def find_python():
    """Find Python executable, preferring venv"""
    venv_python = os.path.join(SCRIPT_DIR, ".venv", "Scripts", "python.exe")
    if os.path.exists(venv_python):
        return venv_python
    return sys.executable

def wait_for_port(port, host='127.0.0.1', timeout=120):
    """Wait for a port to become available"""
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((host, port))
            sock.close()
            if result == 0:
                return True
        except:
            pass
        time.sleep(1)
    return False

def stop_gradio_server():
    """Stop the running Gradio server"""
    global server_process, server_url
    if server_process:
        print("[Chatterbox] Stopping server...")
        try:
            # Try graceful termination first
            server_process.terminate()
            try:
                server_process.wait(timeout=3)
            except subprocess.TimeoutExpired:
                server_process.kill() # Force kill if stuck
        except Exception as e:
            print(f"[Chatterbox] Error stopping server: {e}")
        server_process = None
        server_url = None
        print("[Chatterbox] Server stopped.")

def start_gradio_server(mode="turbo"):
    """Start the Gradio server and return the URL"""
    global server_process, server_url
    
    # Ensure any previous server is stopped
    stop_gradio_server()
    
    scripts = {

        "turbo": "gradio_tts_turbo_app.py",
        "standard": "gradio_tts_app.py",
        "multilingual": "multilingual_app.py",
        "voice_conversion": "gradio_vc_app.py"
    }
    
    script_file = scripts.get(mode, scripts["turbo"])
    script_path = os.path.join(SCRIPT_DIR, script_file)
    python_exe = find_python()
    
    print(f"[Chatterbox] Launching {mode} mode...")
    
    # Set up environment
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    
    # Inject Output Directory from Settings
    settings = load_settings()
    output_dir = settings.get("output_dir")
    if output_dir:
        print(f"[Chatterbox] Output Directory: {output_dir}")
        env["CHATTERBOX_OUTPUT_DIR"] = output_dir
    
    try:
        server_process = subprocess.Popen(
            [python_exe, script_path],
            cwd=SCRIPT_DIR,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding='utf-8', # Force UTF-8 logging to handle emojis on Windows
            errors='replace', # Replace invalid characters instead of crashing
            bufsize=1,
            env=env,
            creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0
        )
        
        # Monitor output in background
        def monitor_output():
            if server_process and server_process.stdout:
                for line in server_process.stdout:
                    if line.strip():
                        print(f"[Server] {line.strip()}")
        
        threading.Thread(target=monitor_output, daemon=True).start()
        
        print(f"[Chatterbox] Waiting for port {DEFAULT_PORT}...")
        if wait_for_port(DEFAULT_PORT):
            url = f"http://127.0.0.1:{DEFAULT_PORT}"
            server_url = url
            print(f"[Chatterbox] Ready at {url}")
            return url
        else:
            print("[Chatterbox] Timeout waiting for server.")
            return None
            
    except Exception as e:
        print(f"[Chatterbox] Failed to launch: {e}")
        return None

def cleanup():
    stop_gradio_server()

atexit.register(cleanup)

def run_desktop_app(initial_mode=None):
    """Main entry point"""
    global main_window
    
    api = Api()
    
    # If no mode specified, start with Dashboard
    start_html = DASHBOARD_HTML
    if initial_mode:
        start_html = LOADING_HTML
    
    main_window = webview.create_window(
        APP_TITLE,
        html=start_html,
        width=WINDOW_WIDTH,
        height=WINDOW_HEIGHT,
        resizable=True,
        min_size=(900, 600),
        js_api=api,
        background_color='#1a1a2e'
    )
    
    # If a specific mode was requested CLI, launch it immediately after window load
    if initial_mode:
        def auto_launch():
            # Give window a moment to appear
            time.sleep(1) 
            api.launch_mode(initial_mode)
        webview.start(auto_launch, debug=True)
    else:
        webview.start(debug=True)

if __name__ == "__main__":
    # Check CLI args
    mode_arg = None
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        if arg in ["turbo", "standard", "multilingual"]:
            mode_arg = arg
        else:
            print(f"Unknown mode: {arg}. Launching dashboard.")
            
    run_desktop_app(mode_arg)
