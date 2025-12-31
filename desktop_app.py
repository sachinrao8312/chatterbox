"""
Chatterbox TTS - Desktop Application
A native desktop app that runs the Gradio TTS server and displays it in a native window.
"""

import webview
import webbrowser
import threading
import subprocess
import sys
import os
import time
import re
import atexit
import socket

# Configuration
APP_TITLE = "Chatterbox TTS"
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_PORT = 7860

# Server process reference
server_process = None
server_url = None


class Api:
    """JavaScript API for the webview"""
    
    def open_in_browser(self):
        """Open the server URL in the default browser"""
        global server_url
        if server_url:
            webbrowser.open(server_url)
            return True
        return False
    
    def get_server_url(self):
        """Get the current server URL"""
        global server_url
        return server_url or ""


def find_python():
    """Find the Python executable, preferring venv"""
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


def read_server_output():
    """Read server output in background"""
    global server_process
    if server_process:
        try:
            for line in server_process.stdout:
                line = line.strip()
                if line:
                    print(f"[Server] {line}")
        except:
            pass


def start_gradio_server(mode="turbo"):
    """Start the Gradio server and return the URL"""
    global server_process, server_url
    
    scripts = {
        "turbo": "gradio_tts_turbo_app.py",
        "standard": "gradio_tts_app.py",
        "multilingual": "multilingual_app.py"
    }
    
    script_path = os.path.join(SCRIPT_DIR, scripts.get(mode, scripts["turbo"]))
    python_exe = find_python()
    
    print(f"[Chatterbox] Starting {mode} mode...")
    print(f"[Chatterbox] Python: {python_exe}")
    print(f"[Chatterbox] Script: {script_path}")
    
    # Set up environment with UTF-8 encoding to handle emojis on Windows
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    
    # Start the server process
    server_process = subprocess.Popen(
        [python_exe, script_path],
        cwd=SCRIPT_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
        env=env,
        encoding="utf-8",
        errors="replace",
        creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0
    )
    
    # Read output in background thread
    output_thread = threading.Thread(target=read_server_output, daemon=True)
    output_thread.start()
    
    print(f"[Chatterbox] Waiting for server on port {DEFAULT_PORT}...")
    
    # Wait for port to be available
    if wait_for_port(DEFAULT_PORT):
        url = f"http://127.0.0.1:{DEFAULT_PORT}"
        server_url = url
        print(f"[Chatterbox] Server ready at: {url}")
        return url
    else:
        print("[Chatterbox] Timeout waiting for server")
        return None


def cleanup():
    """Clean up server process on exit"""
    global server_process
    if server_process:
        print("[Chatterbox] Shutting down server...")
        try:
            server_process.terminate()
            server_process.wait(timeout=5)
        except:
            try:
                server_process.kill()
            except:
                pass
        print("[Chatterbox] Server stopped")


# Register cleanup
atexit.register(cleanup)


def create_loading_html():
    """Create a beautiful loading page"""
    return """
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
                justify-content: center;
                align-items: center;
                color: white;
            }
            
            .container {
                text-align: center;
                padding: 40px;
            }
            
            .logo {
                font-size: 72px;
                margin-bottom: 20px;
                animation: pulse 2s ease-in-out infinite;
            }
            
            @keyframes pulse {
                0%, 100% { transform: scale(1); }
                50% { transform: scale(1.1); }
            }
            
            h1 {
                font-size: 36px;
                font-weight: 300;
                margin-bottom: 10px;
                background: linear-gradient(90deg, #00d4ff, #00ff88);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
            }
            
            .subtitle {
                font-size: 16px;
                color: #888;
                margin-bottom: 40px;
            }
            
            .loader {
                width: 60px;
                height: 60px;
                border: 3px solid rgba(0, 212, 255, 0.2);
                border-top-color: #00d4ff;
                border-radius: 50%;
                animation: spin 1s linear infinite;
                margin: 0 auto 30px;
            }
            
            @keyframes spin {
                to { transform: rotate(360deg); }
            }
            
            .status {
                font-size: 14px;
                color: #00ff88;
                animation: blink 1.5s ease-in-out infinite;
            }
            
            @keyframes blink {
                0%, 100% { opacity: 1; }
                50% { opacity: 0.5; }
            }
            
            .tips {
                margin-top: 40px;
                padding: 20px;
                background: rgba(255,255,255,0.05);
                border-radius: 12px;
                max-width: 400px;
            }
            
            .tips h3 {
                font-size: 14px;
                color: #00d4ff;
                margin-bottom: 10px;
            }
            
            .tips p {
                font-size: 12px;
                color: #666;
                line-height: 1.6;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="logo">🎙️</div>
            <h1>Chatterbox TTS</h1>
            <p class="subtitle">Text-to-Speech Desktop Application</p>
            
            <div class="loader"></div>
            <p class="status">Loading AI models... This may take a minute on first launch.</p>
            
            <div class="tips">
                <h3>💡 Did you know?</h3>
                <p>Chatterbox can clone any voice from just a few seconds of audio! 
                   Upload a reference clip to match the speaking style.</p>
            </div>
        </div>
    </body>
    </html>
    """


def create_main_page_with_toolbar(gradio_url):
    """Create a page that embeds Gradio with a toolbar for opening in browser"""
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            
            body {{
                font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, sans-serif;
                height: 100vh;
                display: flex;
                flex-direction: column;
                background: #1a1a2e;
            }}
            
            .toolbar {{
                background: linear-gradient(90deg, #1a1a2e, #16213e);
                padding: 8px 16px;
                display: flex;
                align-items: center;
                justify-content: space-between;
                border-bottom: 1px solid rgba(0, 212, 255, 0.2);
                flex-shrink: 0;
            }}
            
            .toolbar-left {{
                display: flex;
                align-items: center;
                gap: 12px;
            }}
            
            .toolbar-logo {{
                font-size: 20px;
            }}
            
            .toolbar-title {{
                color: #00d4ff;
                font-size: 14px;
                font-weight: 500;
            }}
            
            .toolbar-url {{
                color: #666;
                font-size: 12px;
                background: rgba(255,255,255,0.05);
                padding: 4px 12px;
                border-radius: 4px;
                font-family: monospace;
            }}
            
            .toolbar-right {{
                display: flex;
                gap: 10px;
            }}
            
            .btn {{
                background: linear-gradient(135deg, #00d4ff, #00b8d4);
                color: #1a1a2e;
                border: none;
                padding: 8px 16px;
                border-radius: 6px;
                font-size: 12px;
                font-weight: 600;
                cursor: pointer;
                display: flex;
                align-items: center;
                gap: 6px;
                transition: all 0.2s ease;
            }}
            
            .btn:hover {{
                transform: translateY(-1px);
                box-shadow: 0 4px 12px rgba(0, 212, 255, 0.3);
            }}
            
            .btn-secondary {{
                background: rgba(255,255,255,0.1);
                color: #ccc;
            }}
            
            .btn-secondary:hover {{
                background: rgba(255,255,255,0.15);
                box-shadow: none;
            }}
            
            iframe {{
                flex: 1;
                width: 100%;
                border: none;
            }}
        </style>
    </head>
    <body>
        <div class="toolbar">
            <div class="toolbar-left">
                <span class="toolbar-logo">🎙️</span>
                <span class="toolbar-title">Chatterbox TTS</span>
                <span class="toolbar-url">{gradio_url}</span>
            </div>
            <div class="toolbar-right">
                <button class="btn" onclick="openInBrowser()">
                    🌐 Open in Chrome
                </button>
                <button class="btn btn-secondary" onclick="copyUrl()">
                    📋 Copy URL
                </button>
            </div>
        </div>
        <iframe src="{gradio_url}" id="gradioFrame"></iframe>
        
        <script>
            function openInBrowser() {{
                pywebview.api.open_in_browser();
            }}
            
            function copyUrl() {{
                navigator.clipboard.writeText("{gradio_url}");
                const btn = event.target;
                const originalText = btn.innerHTML;
                btn.innerHTML = "✅ Copied!";
                setTimeout(() => btn.innerHTML = originalText, 1500);
            }}
        </script>
    </body>
    </html>
    """


def run_desktop_app(mode="turbo"):
    """Main function to run the desktop application"""
    
    api = Api()
    
    # Create initial loading window
    window = webview.create_window(
        APP_TITLE,
        html=create_loading_html(),
        width=WINDOW_WIDTH,
        height=WINDOW_HEIGHT,
        resizable=True,
        min_size=(800, 600),
        js_api=api
    )
    
    def load_gradio():
        """Start server and load Gradio UI"""
        url = start_gradio_server(mode)
        if url:
            # Small delay to ensure server is fully ready
            time.sleep(2)
            # Load the page with toolbar
            window.load_html(create_main_page_with_toolbar(url))
        else:
            window.load_html("""
                <html>
                <body style="background:#1a1a2e;color:white;display:flex;justify-content:center;align-items:center;height:100vh;font-family:sans-serif;">
                    <div style="text-align:center">
                        <h1 style="color:#ff4757">❌ Failed to Start Server</h1>
                        <p>Check the console for error details.</p>
                    </div>
                </body>
                </html>
            """)
    
    # Start server in background after window is created
    def on_loaded():
        threading.Thread(target=load_gradio, daemon=True).start()
    
    # Start webview
    webview.start(on_loaded, debug=False)


if __name__ == "__main__":
    # Default to turbo mode, or accept command line argument
    mode = sys.argv[1] if len(sys.argv) > 1 else "turbo"
    
    if mode not in ["turbo", "standard", "multilingual"]:
        print(f"Unknown mode: {mode}")
        print("Available modes: turbo, standard, multilingual")
        sys.exit(1)
    
    print(f"\n{'='*50}")
    print(f"  Chatterbox TTS Desktop App")
    print(f"  Mode: {mode}")
    print(f"{'='*50}\n")
    
    run_desktop_app(mode)
