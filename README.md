# Feishu OpenCode Bridge

🇨🇳 [简体中文](./README_zh.md) | 🇺🇸 [English](./README.md)

---

## 🎯 What Does It Solve?

Tired of complex bot configuration?

**Feishu OpenCode Bridge** runs with a **single double-click** — no complicated setup required, as simple as using OpenClaw.

---

## ✨ Why Choose It?

| Comparison | Traditional Solutions | Feishu OpenCode Bridge |
|------------|----------------------|------------------------|
| Setup | Requires coding & environment | **Double-click to run** |
| Files | Multiple complex scripts | **Only 2 files** |
| Dependencies | Complex environment setup | **pip install only** |
| Maintenance | Large codebase hard to maintain | **Single file, clean & simple** |

---

## 🚀 Get Started in 5 Minutes

### Step 1: Download & Install Dependencies

```bash
git clone https://github.com/Malcolm3299/feishu_opencode_bridge.git
cd feishu_opencode_bridge
pip install -r requirements.txt
```

### Step 2: Configure

1. Copy `config.py.example` → `config.py`
2. Fill in your Feishu bot credentials (same as OpenClaw Feishu bot setup)
3. Set OpenCode path

### Step 3: Run with One Click

```
Double-click run.bat
```

**Done!** Send a message to your bot and try it out!

---

## 📸 Demo

### Feishu Chat Interface
![Feishu Chat](./images/feishu.jpg)

### Code Highlighting Example
![Code Example](./images/log&example.jpg)

### Run Control Interface
![Run Control](./images/run_control.jpg)

---

## ⚙️ Configuration

```python
# Required
APP_ID = "cli_xxxxx"           # From Feishu Open Platform
APP_SECRET = "xxxxxxxxxxxxx"    # From Feishu Open Platform
OPENCOD_BIN = "opencode"       # OpenCode command

# Optional
MODEL = "opencode/minimax-m2.5-free"
OPENCOD_PORT = 4096
```

> 💡 **Tip**: Feishu bot configuration is identical to [OpenClaw Feishu setup](https://docs.openclaw.ai/) — no extra learning required!

---

## 🏗 Project Structure

```
feishu_opencode_bridge/
├── bridge.py           # Core program (just this one)
├── config.py.example   # Config template
├── run.bat            # Double-click to run
├── requirements.txt   # Python dependencies
├── LICENSE          # MIT License
└── images/         # Demo screenshots
    ├── feishu.jpg
    ├── log&example.jpg
    └── run_control.jpg
```

---

## ❓ FAQ

**Q: Failed to start?**
A: Make sure Python 3.8+ is installed and you ran `pip install -r requirements.txt`

**Q: Bot not responding?**
A: Check if `im.message.receive_v1` event subscription is enabled in Feishu Open Platform

**Q: OpenCode timeout?**
A: Check your network connection or try restarting OpenCode service

---

## 📄 License

[MIT License](./LICENSE)

---

## 🤝 Contributing

Found a bug? Welcome to submit an [Issue](https://github.com/Malcolm3299/feishu_opencode_bridge/issues)!

Have improvements? Pull Requests are welcome!
