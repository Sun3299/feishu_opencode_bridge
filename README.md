# Feishu OpenCode Bridge

🔗 A relay service that forwards Feishu (Lark) messages to OpenCode AI and returns beautifully rendered results.

🇨🇳 [简体中文](./README_zh.md) | 🇺🇸 [English](./README.md)

---

## ✨ Features

### Core Functionality

- **Message Forwarding** - Automatically forwards Feishu private messages to OpenCode
- **Markdown Rendering** - Uses Feishu interactive cards with full Markdown support (code blocks, bold, italic, etc.)
- **Message Queue** - Serial processing to maintain message order
- **Single Instance Protection** - Prevents multiple instances from running
- **Logging System** - Dual output to console and log file

### Technical Highlights

- Asynchronous message processing without blocking WebSocket
- Automatic ANSI color code cleanup
- Smart text formatting for Feishu display
- Interactive command-line menu for easy management

---

## 🚀 Quick Start

### Requirements

- Python 3.8+
- [OpenCode CLI](https://github.com/opencode-ai/opencode) (installed and configured)
- Feishu Enterprise App

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/Malcolm3299/feishu-opencode-bridge.git
cd feishu-opencode-bridge

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure
cp config.py.example config.py
# Edit config.py with your Feishu credentials and OpenCode path

# 4. Run
# Windows
run.bat

# Linux / Mac
python3 bridge.py
```

---

## ⚙️ Configuration

Edit `config.py`:

```python
# ============== Required ==============

# Feishu App Credentials
APP_ID = "cli_xxxxx"           # Get from Feishu Open Platform
APP_SECRET = "xxxxxxxxxxxxx"    # Get from Feishu Open Platform

# OpenCode Settings
OPENCOD_BIN = "opencode"       # or full path
MODEL = "opencode/minimax-m2.5-free"

# ============== Optional ==============

OPENCOD_PORT = 4096    # OpenCode server port
ENABLE_LOG = True    # Enable logging
```

### Getting Feishu Credentials

1. Go to [Feishu Open Platform](https://open.feishu.cn/)
2. Create an Enterprise App
3. Get App ID and App Secret
4. Enable Bot capability
5. Subscribe to message event `im.message.receive_v1`

---

## 📖 Usage

### Starting

```bash
# Windows: Double-click run.bat or run in command line
python bridge.py
```

### Interactive Menu

When an existing instance is detected:

```
============================================================
  Feishu <-> OpenCode Bridge is already running!
============================================================
  Current process PID: 12345

  Choose an option:
  [1] Kill this process and restart
  [2] Kill all Python processes and restart
  [3] Exit
============================================================
Enter option (1/2/3):
```

### Logs

Logs are saved to `bridge.log`.

---

## 🏗 Project Structure

```
feishu-opencode-bridge/
├── bridge.py           # Main program
├── config.py.example   # Configuration template
├── run.bat             # Windows launcher
├── requirements.txt    # Python dependencies
├── LICENSE            # MIT License
└── README_zh.md      # Chinese README
```

---

## ❓ FAQ

**Q: "App not found" error on startup?**

A: Check if `APP_ID` and `APP_SECRET` in `config.py` are correct.

**Q: OpenCode timeout?**

A: Try adjusting `OPENCOD_PORT` or check your network connection.

**Q: How to get Feishu credentials?**

A: Go to [Feishu Open Platform](https://open.feishu.cn/), create an app, and get App ID and App Secret.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 🤝 Contributing

Issues and Pull Requests are welcome!
