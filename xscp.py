#!/usr/bin/env python3
import argparse
import subprocess
import sys
import os
from datetime import datetime
from pathlib import Path

LOG_FILE = "smartcp.log"

# ------------------- SCP & Logging -------------------

def log_transfer(source, dest, port, status):
    """Write transfer details to log file"""
    with open(LOG_FILE, "a") as log:
        log.write(f"{datetime.now()} | SRC: {source} | DEST: {dest} | PORT: {port} | STATUS: {status}\n")

def get_last_destination():
    """Fetch last destination from logs"""
    if not os.path.exists(LOG_FILE):
        return None
    with open(LOG_FILE, "r") as log:
        lines = log.readlines()
        for line in reversed(lines):
            if "DEST:" in line:
                parts = line.split("|")
                for p in parts:
                    if "DEST:" in p:
                        return p.replace("DEST:", "").strip()
    return None

def run_scp(source, dest, port):
    """Run SCP command with error handling and return a dictionary"""
    try:
        cmd = ["scp", "-P", str(port), source, dest]
        result = subprocess.run(cmd, capture_output=True, text=True, check=False)

        if result.returncode == 0:
            print("[✅] Transfer successful!")
            log_transfer(source, dest, port, "SUCCESS")
            return {"success": True, "message": "Transfer successful!"}
        else:
            print(f"[❌] Transfer failed: {result.stderr.strip()}")
            log_transfer(source, dest, port, "FAILED")
            return {"success": False, "message": result.stderr.strip()}

    except Exception as e:
        print(f"[ERROR] {e}")
        log_transfer(source, dest, port, "ERROR")
        return {"success": False, "message": str(e)}

# ------------------- TUI -------------------

def list_files_tui(path="."):
    """List files for the TUI"""
    return os.listdir(path)

def print_banner():
    """Prints the TUI banner with a purple gradient effect"""
    colors = [93, 99, 105, 111, 117, 123]  # Purple shades
    banner_lines = [
        "╔═══════════════════════════════╗",
        "║              XScp             ║",
        "║ Simple SCP Tool designed for  ║",
        "║          simplicity           ║",
        "║            (⌐■_■)             ║",
        "╚═══════════════════════════════╝"
    ]
    for i, line in enumerate(banner_lines):
        color = colors[i % len(colors)]
        print(f"\033[38;5;{color}m{line}\033[0m")

def show_menu():
    os.system("cls" if os.name == "nt" else "clear")
    print_banner()
    print("\n1) Copy File")
    print("2) Change Directory")
    print("3) View Transfer Log")
    print("4) Exit\n")

def view_log():
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as log:
            print("=== Transfer History (Last 10) ===")
            for line in log.readlines()[-10:]:
                print(line.strip())
    else:
        print("No transfers logged yet.")
    input("\nPress Enter to return to menu...")

def tui_mode():
    current_path = os.getcwd()
    while True:
        show_menu()
        choice = input("Choose an option: ")

        if choice == "1":
            files = list_files_tui(current_path)
            print(f"\n📂 Current Directory: {current_path}")
            for idx, f in enumerate(files, 1):
                print(f" {idx}. {f}")
            filename = input("Enter filename to copy (or full path): ").strip()
            source = filename if os.path.isabs(filename) else os.path.join(current_path, filename)
            last_dest = get_last_destination()
            dest_prompt = f"Enter destination [default: {last_dest}]: " if last_dest else "Enter destination (user@host:/path): "
            dest = input(dest_prompt).strip() or (last_dest if last_dest else "")
            port = input("Enter port [default 22]: ").strip() or "22"
            run_scp(source, dest, port)
            input("\nPress Enter to return to menu...")

        elif choice == "2":
            new_dir = input("Enter directory path (relative or absolute): ").strip()
            try:
                # Change directory and resolve to absolute path
                os.chdir(os.path.join(current_path, new_dir))
                current_path = os.getcwd()
                print(f"[📂] Changed directory to: {current_path}")
            except FileNotFoundError:
                print("[❌] Invalid directory.")
            input("\nPress Enter to continue...")

        elif choice == "3":
            view_log()

        elif choice == "4":
            print("Goodbye 👋")
            sys.exit(0)
        else:
            print("Invalid option!")
            input("\nPress Enter to return to menu...")

# ------------------- CLI -------------------

def cli_mode(args):
    run_scp(args.source, args.dest, args.port)

# ------------------- Web UI -------------------

def webui_mode():
    try:
        from flask import Flask, jsonify, request, render_template_string
    except ImportError:
        print("[ERROR] Flask is not installed. To use the Web UI, run: pip install Flask")
        sys.exit(1)

    app = Flask(__name__)
    
    # Define a safe base directory (user's home directory)
    SAFE_BASE_DIR = os.path.expanduser("~")

    HTML_PAGE = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>XScp Web UI</title>
        <style>
            :root {
                --bg-dark: #1e1e2f; --bg-med: #2e2e4f; --text-light: #f0f0f0;
                --grad-start: #a100ff; --grad-end: #6f00ff;
            }
            body { background-color: var(--bg-dark); color: var(--text-light); font-family: monospace; margin: 0; padding: 15px;}
            .container { max-width: 800px; margin: 20px auto; padding: 20px; background: var(--bg-med); border-radius: 8px; }
            h1 { background: linear-gradient(90deg, var(--grad-start), var(--grad-end)); -webkit-background-clip: text; color: transparent; text-align: center; margin-top: 0; }
            h2 { border-bottom: 2px solid var(--grad-start); padding-bottom: 5px; margin-top: 30px; }
            .ascii-face { text-align: center; font-size: 1.5em; margin-bottom: 20px; }
            label { display: block; margin-top: 10px; }
            input, select { background: var(--bg-dark); color: var(--text-light); border: 1px solid #444; padding: 8px; margin-top: 5px; width: calc(100% - 18px); border-radius: 4px; }
            button { background: linear-gradient(90deg, var(--grad-start), var(--grad-end)); color: var(--text-light); border: none; padding: 10px 15px; cursor: pointer; border-radius: 4px; width: 100%; margin-top: 15px; font-size: 1em; }
            button:hover { opacity: 0.9; transform: scale(1.01); }
            #file-explorer { background: var(--bg-dark); border: 1px solid #444; border-radius: 4px; margin-top: 10px; }
            #breadcrumbs { padding: 8px; background: #3a3a5f; border-bottom: 1px solid #444; font-size: 0.9em; white-space: nowrap; overflow-x: auto; }
            .breadcrumb-item { cursor: pointer; color: #aaa; } .breadcrumb-item:hover { color: var(--text-light); }
            #file-list { max-height: 300px; overflow-y: auto; padding: 5px; }
            .explorer-item { padding: 6px 10px; cursor: pointer; border-radius: 3px; display: flex; align-items: center; gap: 8px; }
            .explorer-item:hover { background-color: #3a3a5f; }
            .explorer-item.selected { background-color: var(--grad-start); }
            pre { background: var(--bg-dark); padding: 10px; border: 1px solid #444; border-radius: 4px; overflow-x: auto; max-height: 200px; }
            #status-message { text-align: center; padding: 10px; margin-top: 15px; border-radius: 4px; display: none; }
            #status-message.success { background: #1a4a1a; } #status-message.error { background: #5a1a1a; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>XScp Web UI</h1>
            <div class="ascii-face">(⌐■_■)</div>
            
            <h2>File Explorer</h2>
            <div id="file-explorer">
                <div id="breadcrumbs"></div>
                <div id="file-list">Loading...</div>
            </div>

            <h2>Copy File</h2>
            <form id="scp-form">
                <label for="source">Source:</label><input type="text" id="source" required/>
                <label for="dest">Destination:</label><input type="text" id="dest" placeholder="user@host:/path" required/>
                <label for="port">Port:</label><input type="number" id="port" value="22"/>
                <button type="submit">Copy File</button>
            </form>
            <div id="status-message"></div>

            <h2>Transfer Log (Last 10)</h2>
            <pre id="log-area">No logs yet.</pre>
        </div>

        <script>
            let currentSelectedFileElement = null;

            async function fetchAndRenderFiles(path = '') {
                const fileListDiv = document.getElementById('file-list');
                fileListDiv.textContent = 'Loading...';
                try {
                    const response = await fetch(`/api/list?path=${encodeURIComponent(path)}`);
                    if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
                    const data = await response.json();

                    renderBreadcrumbs(data.current_path);
                    fileListDiv.innerHTML = ''; // Clear loading message

                    // Add "Up" directory link
                    if (data.parent_path) {
                        const upEl = createExplorerItem({ name: '..', path: data.parent_path, type: 'folder' }, '⬆️');
                        fileListDiv.appendChild(upEl);
                    }
                    
                    data.items.forEach(item => {
                        const icon = item.type === 'folder' ? '📂' : '📄';
                        const itemEl = createExplorerItem(item, icon);
                        fileListDiv.appendChild(itemEl);
                    });
                } catch (error) {
                    fileListDiv.textContent = `Error loading files: ${error.message}`;
                }
            }
            
            function createExplorerItem(item, icon) {
                const el = document.createElement('div');
                el.className = 'explorer-item';
                el.innerHTML = `<span>${icon}</span><span>${item.name}</span>`;
                el.dataset.path = item.path;
                el.dataset.type = item.type;

                el.addEventListener('click', () => {
                    if (item.type === 'folder') {
                        fetchAndRenderFiles(item.path);
                    } else { // It's a file
                        document.getElementById('source').value = item.path;
                        if (currentSelectedFileElement) {
                            currentSelectedFileElement.classList.remove('selected');
                        }
                        el.classList.add('selected');
                        currentSelectedFileElement = el;
                    }
                });
                return el;
            }
            
            function renderBreadcrumbs(fullPath) {
                const breadcrumbsDiv = document.getElementById('breadcrumbs');
                breadcrumbsDiv.innerHTML = '';
                const parts = fullPath.split(/[\\/]/).filter(p => p);
                let currentPath = '';

                // Add root link
                const rootEl = document.createElement('span');
                rootEl.className = 'breadcrumb-item';
                rootEl.textContent = '🏠 /';
                rootEl.onclick = () => fetchAndRenderFiles('/');
                breadcrumbsDiv.appendChild(rootEl);
                
                parts.forEach((part, index) => {
                    currentPath += part + '/';
                    const partEl = document.createElement('span');
                    partEl.className = 'breadcrumb-item';
                    partEl.textContent = `${part} /`;
                    partEl.dataset.path = currentPath;
                    partEl.onclick = () => fetchAndRenderFiles(partEl.dataset.path);
                    breadcrumbsDiv.appendChild(partEl);
                });
            }

            async function fetchLog() {
                try {
                    const response = await fetch('/api/log');
                    const data = await response.json();
                    const logArea = document.getElementById('log-area');
                    logArea.textContent = data.log.length > 0 ? data.log.join('\\n') : 'No logs yet.';
                } catch (error) {
                    console.error('Failed to fetch log:', error);
                }
            }

            async function fetchLastDestination() {
                try {
                    const response = await fetch('/api/last_destination');
                    const data = await response.json();
                    if (data.destination) {
                        document.getElementById('dest').value = data.destination;
                    }
                } catch(error) {
                    console.error('Failed to fetch last destination:', error);
                }
            }
            
            document.getElementById('scp-form').addEventListener('submit', async (e) => {
                e.preventDefault();
                const src = document.getElementById('source').value;
                const dest = document.getElementById('dest').value;
                const port = document.getElementById('port').value;
                const statusDiv = document.getElementById('status-message');

                statusDiv.textContent = 'Transferring...';
                statusDiv.className = '';
                statusDiv.style.display = 'block';

                try {
                    const response = await fetch('/api/scp', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ source: src, dest: dest, port: port })
                    });
                    const data = await response.json();
                    
                    statusDiv.textContent = data.message;
                    statusDiv.classList.add(data.success ? 'success' : 'error');
                } catch(error) {
                    statusDiv.textContent = `Error: ${error.message}`;
                    statusDiv.classList.add('error');
                } finally {
                    fetchLog(); // Refresh log after every attempt
                    setTimeout(() => { statusDiv.style.display = 'none'; }, 5000);
                }
            });

            // Initial load
            window.onload = () => {
                fetchAndRenderFiles();
                fetchLog();
                fetchLastDestination();
            };
        </script>
    </body>
    </html>
    """

    @app.route("/")
    def index():
        return render_template_string(HTML_PAGE)

    @app.route("/api/list")
    def list_dir_endpoint():
        req_path = request.args.get('path', SAFE_BASE_DIR)
        
        # Security: Resolve the path and ensure it's within the safe base directory
        try:
            current_path = Path(req_path).resolve()
            if not str(current_path).startswith(str(Path(SAFE_BASE_DIR).resolve())):
                current_path = Path(SAFE_BASE_DIR).resolve()
        except Exception:
            current_path = Path(SAFE_BASE_DIR).resolve()

        if not current_path.is_dir():
            current_path = current_path.parent

        items = []
        try:
            for entry in os.scandir(current_path):
                items.append({
                    "name": entry.name,
                    "path": entry.path,
                    "type": "folder" if entry.is_dir() else "file"
                })
        except PermissionError:
            pass # Ignore directories we can't read
        
        # Sort folders first, then files, both alphabetically
        items.sort(key=lambda x: (x['type'] != 'folder', x['name'].lower()))

        parent_path = str(current_path.parent) if str(current_path) != str(Path(SAFE_BASE_DIR).resolve()) else None

        return jsonify({
            "current_path": str(current_path),
            "parent_path": parent_path,
            "items": items
        })

    @app.route("/api/log")
    def log_endpoint():
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE) as f:
                lines = f.readlines()[-10:]
        else:
            lines = []
        return jsonify({"log": [line.strip() for line in lines]})
    
    @app.route("/api/last_destination")
    def last_dest_endpoint():
        return jsonify({"destination": get_last_destination()})

    @app.route("/api/scp", methods=["POST"])
    def scp_endpoint():
        data = request.json
        result = run_scp(data["source"], data["dest"], data.get("port", 22))
        return jsonify(result)

    print("🚀 Web UI running at http://127.0.0.1:5000")
    app.run(host="127.0.0.1", port=5000)

# ------------------- Main -------------------

def main():
    parser = argparse.ArgumentParser(
        description="XScp - A simple SCP tool with CLI, TUI, and Web interfaces.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("-s", "--source", help="Source file path")
    parser.add_argument("-d", "--dest", help="Destination (e.g., user@host:/path)")
    parser.add_argument("-p", "--port", type=int, default=22, help="SSH Port (default: 22)")
    parser.add_argument("-w", "--web", action="store_true", help="Launch the graphical Web UI")
    args = parser.parse_args()

    # If no arguments are provided, default to TUI mode.
    if not any(vars(args).values()):
        tui_mode()
    elif args.web:
        webui_mode()
    elif args.source and args.dest:
        cli_mode(args)
    else:
        # If some args are present but not enough for CLI mode (and not --web), show TUI.
        tui_mode()

if __name__ == "__main__":
    main()