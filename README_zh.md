# Feishu OpenCode Bridge

🔗 飞书机器人桥接器 - 将飞书消息转发到 OpenCode AI 并返回渲染后的结果

🇨🇳 [简体中文](./README_zh.md) | 🇺🇸 [English](./README.md)

---

## ✨ 功能特性

### 核心功能

- **消息转发** - 将飞书私聊消息自动转发到 OpenCode 处理
- **Markdown 渲染** - 使用飞书交互式卡片，支持代码块、粗体、斜体等格式
- **消息队列** - 串行处理多条消息，避免乱序
- **单实例保护** - 防止重复启动同一个桥接器
- **日志系统** - 同时输出到控制台和日志文件

### 技术亮点

- 异步消息处理，不阻塞 WebSocket 连接
- 自动清理 ANSI 颜色转义码
- 智能文本清洗，适配飞书显示
- 交互式命令行菜单，方便管理

---

## 🚀 快速开始

### 环境要求

- Python 3.8+
- [OpenCode CLI](https://github.com/opencode-ai/opencode) (需安装并配置)
- 飞书企业自建应用

### 安装步骤

```bash
# 1. 克隆项目
git clone https://github.com/Malcolm3299/feishu-opencode-bridge.git
cd feishu-opencode-bridge

# 2. 安装依赖
pip install -r requirements.txt

# 3. 配置
cp config.py.example config.py
# 编辑 config.py，填入你的飞书应用凭证和 OpenCode 路径

# 4. 运行
# Windows
run.bat

# Linux / Mac
python3 bridge.py
```

---

## ⚙️ 配置说明

编辑 `config.py`:

```python
# ============== 必填配置 ==============

# 飞书应用凭证
APP_ID = "cli_xxxxx"           # 飞书开放平台获取
APP_SECRET = "xxxxxxxxxxxxx"   # 飞书开放平台获取

# OpenCode 配置
OPENCOD_BIN = "opencode"       # 或完整路径
MODEL = "opencode/minimax-m2.5-free"

# ============== 可选配置 ==============

OPENCOD_PORT = 4096    # OpenCode 服务端口
ENABLE_LOG = True    # 是否启用日志
```

### 获取飞书应用凭证

1. 前往 [飞书开放平台](https://open.feishu.cn/)
2. 创建企业自建应用
3. 获取 App ID 和 App Secret
4. 配置机器人能力
5. 订阅消息事件 `im.message.receive_v1`

---

## 📖 使用说明

### 启动

```bash
# Windows 用户双击 run.bat 或在命令行运行
python bridge.py
```

### 交互式菜单

当检测到已有实例运行时，会显示菜单:

```
============================================================
  Feishu <-> OpenCode Bridge 已经在运行中！
============================================================
  当前运行的进程 PID: 12345

  请选择操作：
  [1] 结束该进程并重启
  [2] 结束所有 Python 进程并重启
  [3] 退出
============================================================
请输入选项 (1/2/3):
```

### 日志文件

日志保存在 `bridge.log`，可以随时查看运行状态。

---

## 🏗 项目结构

```
feishu-opencode-bridge/
├── bridge.py           # 主程序
├── config.py.example   # 配置模板
├── run.bat             # Windows 启动脚本
├── requirements.txt    # Python 依赖
├── LICENSE            # MIT 许可证
└── README.md          # English README
```

---

## ❓ 常见问题

**Q: 启动报错 "App not found"?**

A: 请检查 `config.py` 中的 `APP_ID` 和 `APP_SECRET` 是否正确。

**Q: OpenCode 调用超时?**

A: 可以尝试调整 `OPENCOD_PORT`，或检查网络连接。

**Q: 如何获取飞书应用凭证?**

A: 前往 [飞书开放平台](https://open.feishu.cn/) 创建应用，获取 App ID 和 App Secret。

---

## 📄 开源协议

本项目采用 [MIT License](LICENSE) 开源。

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！
