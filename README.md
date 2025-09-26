

---



# XScp - Simple SCP Tool

**XScp** is a multi-functional SCP (Secure Copy Protocol) tool designed to make file transfers to remote SSH servers easier and more user-friendly.

---
![[Pasted image 20250927001928.png]]

***

>I created this tool while experimenting with SCP. I realized that typing full paths repeatedly and copying files between specific locations can be tedious. **XScp was originally developed to manage my homelab server**, making copying files simpler and more efficient via SCP. The project, **Vibe-coded**, is specifically meant for **homelab usage**, providing a streamlined workflow for transferring files and managing directories remotely.


### **It Provides**:

- **Persistent logs** of previously used paths for easy recall.
    
- **Multiple interfaces**: CLI, TUI, and Web UI.
    
- **Cross-platform support** (Windows client to Debian-based Linux servers).
    

This is my **one-way tool** to copy files remotely to my SSH server. Once you specify the path, the logs make future transfers faster and easier.

---

## Features

- Copy files via **CLI, TUI, or Web UI**
    
- Persistent **transfer logs**
    
- Recall last-used destination paths
    
- Interactive file listing in TUI
    
- Web-based file explorer with SCP transfer
    
- **Homelab-friendly**: designed to manage servers and simplify file operations
    
- Cross-platform support (Linux, macOS, Windows)
    

---

## Installation

### **1. Clone the repository**

```bash
git clone https://github.com/yourusername/XScp.git
cd XScp
```

### **2. Setup Python Virtual Environment**

#### Create the environment:

```bash
# Linux / macOS
python3 -m venv venv

# Windows (PowerShell or CMD)
python -m venv venv
```

#### Activate the environment:

```bash
# Linux / macOS
source venv/bin/activate

# Windows PowerShell
venv\Scripts\Activate.ps1

# Windows CMD
venv\Scripts\activate.bat
```

#### Install required packages:

```bash
pip install -r requirements.txt
```

> Required package: `Flask` for Web UI.

#### Deactivate environment:

```bash
deactivate
```

---

## Usage

XScp supports **three modes**: CLI, TUI (Text User Interface), and Web UI.

### **1. TUI Mode (Default)**

Simply run:

```bash
python xscp.py
```

You will see a menu:

1. Copy File
    
2. Change Directory
    
3. View Transfer Log
    
4. Exit
    

- Navigate files in the current directory.
    
- Specify a source file and destination (last-used path is auto-suggested).
    
- Logs will persist in `smartcp.log`.
    

---

### **2. CLI Mode**

Run the tool directly from the command line:

```bash
python xscp.py -s /path/to/source/file -d user@host:/destination/path -p 22
```

- `-s` or `--source`: Source file path
    
- `-d` or `--dest`: Destination (`user@host:/path`)
    
- `-p` or `--port`: SSH port (default: 22)
    

Example:

```bash
python xscp.py -s ./myfile.txt -d root@192.168.1.100:/home/root/
```

---

### **3. Web UI Mode**

Launch a web-based interface:

```bash
python xscp.py --web
```

- Open browser at: `http://127.0.0.1:5000`
    
- Features:
    
    - Interactive file explorer
        
    - SCP transfer form
        
    - View last 10 transfer logs
        
    - Auto-suggests last-used destination path
        

---

## Logs

- All transfers are logged in `smartcp.log` with timestamp, source, destination, port, and status.
    
- TUI and Web UI allow quick access to the last 10 logs.
    
- The last destination path is saved for faster reuse.
    

---

## Cross-Platform Notes

- **Linux / macOS**: Ensure `scp` command is installed (usually included with OpenSSH).
    
- **Windows**: If using Windows 10/11, OpenSSH client should be enabled (`Settings → Apps → Optional Features → OpenSSH Client`).
    
- **Flask** required for Web UI: `pip install Flask`.
    

---

## Example Workflow

**Step 1:** Activate environment

```bash
source venv/bin/activate   # Linux / macOS
venv\Scripts\Activate.ps1  # Windows PowerShell
```

**Step 2:** Launch TUI

```bash
python xscp.py
```

**Step 3:** Navigate directories, select file, transfer, and check logs.

**Step 4:** Deactivate environment

```bash
deactivate
```

---

## Requirements

- Python 3.10+
    
- Flask (for Web UI)
    
- OpenSSH (`scp`) installed on client and server
    

Install Flask:

```bash
pip install Flask
```

---


