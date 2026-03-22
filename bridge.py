#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Feishu <-> OpenCode Bridge
飞书机器人桥接器 - 将飞书消息转发到 OpenCode 并返回结果

功能:
- 单实例运行保护
- 消息队列（串行处理）
- 飞书交互式卡片（支持 Markdown 渲染）
- 日志输出
"""
import os
import sys
import io
import builtins

# 尝试导入配置
try:
    from config import (
        APP_ID, APP_SECRET, OPENCOD_BIN, MODEL,
        BOT_NAME, OPENCOD_PORT, ENABLE_LOG
    )
except ImportError:
    print("错误: 请先复制 config.py.example 为 config.py 并填写配置！")
    sys.exit(1)

# 日志文件
LOG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bridge.log")

# 重定向所有输出到文件
def setup_logging():
    """同时输出到控制台和日志文件"""
    import datetime
    _original_print = builtins.print
    def dual_print(*args, **kwargs):
        msg = " ".join(str(a) for a in args)
        _original_print(msg)
        if ENABLE_LOG:
            try:
                with open(LOG_FILE, "a", encoding="utf-8") as f:
                    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
                    f.write(f"[{timestamp}] {msg}\n")
            except:
                pass
    builtins.print = dual_print

setup_logging()

# 恢复 stdout/stderr UTF-8 支持
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

import lark_oapi as lark
import queue
import threading
from lark_oapi.ws.client import Client
import json
import subprocess
import re
import time
import socket
import urllib.request

# 单实例锁文件
LOCK_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".bridge.lock")


def acquire_single_instance():
    """确保只有一个实例在运行"""
    current_pid = os.getpid()

    if os.path.exists(LOCK_FILE):
        try:
            with open(LOCK_FILE, 'r') as f:
                old_pid = f.read().strip()

            if old_pid and int(old_pid) == current_pid:
                print(f"[单例] 检测到重入，PID: {current_pid}")
                return True

            import subprocess
            try:
                result = subprocess.run(
                    ['powershell', '-Command', f'(Get-Process -Id {old_pid} -ErrorAction SilentlyContinue).Id'],
                    capture_output=True, text=True, timeout=5
                )
                running_pid = result.stdout.strip()
                if running_pid:
                    print("")
                    print("=" * 60)
                    print(f"  {BOT_NAME} 已经在运行中！")
                    print("=" * 60)
                    print(f"  当前运行的进程 PID: {old_pid}")
                    print("")
                    print("  请选择操作：")
                    print("  [1] 结束该进程并重启")
                    print("  [2] 结束所有 Python 进程并重启")
                    print("  [3] 退出")
                    print("=" * 60)
                    choice = input("请输入选项 (1/2/3): ").strip()

                    if choice == "1":
                        print(f"  正在结束进程 {old_pid} ...")
                        subprocess.run(['taskkill', '/F', '/PID', old_pid], capture_output=True)
                        print("  进程已结束")
                    elif choice == "2":
                        print("  正在结束所有 Python 进程 ...")
                        subprocess.run(['taskkill', '/F', '/IM', 'python.exe'], capture_output=True)
                        print("  所有 Python 进程已结束")
                    else:
                        print("  退出")
                        sys.exit(0)

                    time.sleep(1)
                    try:
                        os.remove(LOCK_FILE)
                    except:
                        pass
                    print("  正在重启 ...")
                    time.sleep(0.5)
                    os.execv(sys.executable, [sys.executable, __file__])

            except:
                pass

            try:
                os.remove(LOCK_FILE)
            except:
                pass

        except:
            pass

    try:
        with open(LOCK_FILE, 'w') as f:
            f.write(str(current_pid))
        print(f"[单例] 已创建锁文件，PID: {current_pid}")
        return True
    except Exception as e:
        print(f"[单例] 无法创建锁文件: {e}")
        return None


def release_single_instance(lock_result):
    """释放单实例锁"""
    try:
        os.remove(LOCK_FILE)
    except:
        pass


def is_port_open(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect(("127.0.0.1", port))
        sock.close()
        return True
    except:
        return False


def auto_start_opencode():
    if not is_port_open(OPENCOD_PORT):
        print(f"[OpenCode] 正在启动服务...")
        subprocess.Popen(
            "opencode serve --port " + str(OPENCOD_PORT),
            shell=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        for i in range(10):
            if is_port_open(OPENCOD_PORT):
                print(f"[OpenCode] 服务已启动 (port {OPENCOD_PORT})")
                return True
            time.sleep(1)
        print("[OpenCode] 启动超时")
    else:
        print(f"[OpenCode] 服务已在运行 (port {OPENCOD_PORT})")
    return True


def clean_text(text):
    """清洗文本格式，适配飞书"""
    if not text:
        return ""

    # 1. 去除 ANSI 颜色转义码
    ansi_escape = re.compile(r'\x1b\[[0-9;]*[a-zA-Z]')
    text = ansi_escape.sub('', text)

    # 2. 去除其他 ANSI 控制字符
    text = re.sub(r'\x1b\[[0-9;]*m', '', text)
    text = re.sub(r'\x1b\][^\x07]*\x07', '', text)
    text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', '', text)

    # 3. 清理 markdown 格式
    text = re.sub(r'```(\w*)\n?(.*?)```', r'\n【代码】\n\2\n【代码结束】', text, flags=re.DOTALL)
    text = re.sub(r'`([^`]+)`', r"'\1'", text)
    text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)
    text = re.sub(r'__([^_]+)__', r'\1', text)
    text = re.sub(r'\*([^*]+)\*', r'\1', text)
    text = re.sub(r'_([^_]+)_', r'\1', text)
    text = re.sub(r'~~([^~]+)~~', r'\1', text)
    text = re.sub(r'^#{1,6}\s+', '', text, flags=re.MULTILINE)
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)

    # 4. 折叠连续空行
    text = re.sub(r'\n{3,}', '\n\n', text)

    # 5. 去除首尾空白
    text = text.strip()

    return text


def call_opencode(text):
    """调用 OpenCode 并获取响应"""
    print(f"[OpenCode] 发送请求: {text[:50]}...")

    cmd = [OPENCOD_BIN, "run", "--model", MODEL, "--"]
    cmd.extend(text.split())

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=120,
            encoding='utf-8',
            errors='replace'
        )

        stdout = clean_text(result.stdout)
        stderr = clean_text(result.stderr)

        print(f"[OpenCode] stdout: {stdout[:100] if stdout else '(empty)'}")
        if stderr:
            print(f"[OpenCode] stderr: {stderr[:100]}")

        response = stdout if stdout else (stderr if stderr else "OpenCode 没有返回任何内容")

        if not response:
            response = "OpenCode 返回了空响应"

        return response

    except subprocess.TimeoutExpired:
        print("[OpenCode] 超时")
        return "[错误] OpenCode 处理超时（120秒）"
    except FileNotFoundError:
        print("[OpenCode] 命令未找到")
        return "[错误] OpenCode 命令未找到，请检查 config.py 中的 OPENCOD_BIN 配置"
    except Exception as e:
        error_msg = str(e).encode('utf-8', errors='replace').decode('utf-8')
        print(f"[OpenCode] 错误: {error_msg}")
        return f"[错误] OpenCode 错误: {error_msg[:100]}"


# ============== 飞书部分 ==============
feishu_token = None
feishu_token_expires = 0


def get_feishu_token():
    global feishu_token, feishu_token_expires
    if feishu_token and time.time() < feishu_token_expires - 60:
        return feishu_token
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    data = json.dumps({"app_id": APP_ID, "app_secret": APP_SECRET}).encode("utf-8")
    req = urllib.request.Request(
        url, data=data,
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST"
    )
    try:
        with urllib.request.urlopen(req) as r:
            result = json.loads(r.read().decode("utf-8"))
            if result.get("code") == 0:
                feishu_token = result["tenant_access_token"]
                feishu_token_expires = time.time() + result.get("expire", 7200)
                return feishu_token
    except Exception as e:
        print(f"[Feishu Token] 错误: {e}")
    return None


def send_reply_to_feishu(chat_id, text):
    """回复飞书消息"""
    token = get_feishu_token()
    if not token:
        print("[Feishu] 无 Token")
        return False

    clean = clean_text(text)

    # 使用 interactive card 格式（支持 markdown 渲染）
    card_content = {
        "schema": "2.0",
        "config": {
            "wide_screen_mode": True
        },
        "body": {
            "elements": [
                {
                    "tag": "markdown",
                    "content": clean
                }
            ]
        }
    }
    msg_type = "interactive"
    content = json.dumps(card_content, ensure_ascii=False)

    url = "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=chat_id"
    data = {
        "receive_id": chat_id,
        "msg_type": msg_type,
        "content": content
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(data, ensure_ascii=False).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json; charset=utf-8"
        },
        method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            result = json.loads(r.read().decode("utf-8"))
            if result.get("code") == 0:
                msg_id = result.get("data", {}).get("message_id")
                print(f"[Feishu] 已发送 (ID: {msg_id})")
                return True
            else:
                print(f"[Feishu] 发送失败: {result.get('msg')}")
    except Exception as e:
        print(f"[Feishu] 发送错误: {e}")
    return False


# ============== 消息队列（线程安全） ==============
msg_queue = queue.Queue()


def queue_worker():
    """后台线程：逐个处理队列中的消息"""
    while True:
        item = msg_queue.get()
        if item is None:
            break
        chat_id, text, message_id = item
        print(f"[Queue] 开始处理: {text[:30]}...")
        try:
            response = call_opencode(text)
            send_reply_to_feishu(chat_id, response)
            print(f"[Queue] 处理完成: {text[:30]}...")
        except Exception as e:
            print(f"[Queue] 处理错误: {e}")
            import traceback
            traceback.print_exc()
        msg_queue.task_done()


worker_thread = threading.Thread(target=queue_worker, daemon=True)
worker_thread.start()


# ============== 事件处理 ==============
processed_messages = set()


def on_p2_im_message_receive_v1(data):
    global processed_messages
    print("[Feishu] 收到消息")

    try:
        event = data.event
        if not event:
            return

        message = event.message
        if not message:
            return

        message_id = message.message_id
        chat_id = message.chat_id
        msg_type = message.message_type
        content = message.content

        if message_id in processed_messages:
            print(f"[Msg] 跳过（自己发的）: {message_id}")
            return
        processed_messages.add(message_id)

        if len(processed_messages) > 100:
            processed_messages = set(list(processed_messages)[-50:])

        print(f"[Msg] Chat: {chat_id}, Type: {msg_type}")

        if msg_type != "text":
            send_reply_to_feishu(chat_id, "抱歉，我只支持文本消息")
            return

        try:
            text = json.loads(content).get("text", "").strip()
        except:
            text = content.strip()

        if not text:
            return

        print(f"[Msg] 内容: {text[:50]}")

        msg_queue.put((chat_id, text, message_id))

    except Exception as e:
        print(f"[ERROR] {e}")
        import traceback
        traceback.print_exc()


# ============== 主程序 ==============
def main():
    print("=" * 50)
    print(f"  {BOT_NAME}")
    print(f"  Model: {MODEL}")
    print("=" * 50)

    lock_result = acquire_single_instance()
    if not lock_result:
        sys.exit(1)

    try:
        auto_start_opencode()

        event_handler = (
            lark.EventDispatcherHandler.builder("", "")
            .register_p2_im_message_receive_v1(on_p2_im_message_receive_v1)
            .build()
        )
        print("[Bridge] 事件处理器创建成功")

        cli = lark.ws.Client(
            APP_ID,
            APP_SECRET,
            event_handler=event_handler,
            log_level=lark.LogLevel.INFO
        )
        print("[Bridge] WebSocket 客户端创建成功")

        print(f"\n[Bridge] 准备就绪，向飞书发消息测试吧！")
        print("=" * 50)

        try:
            cli.start()
        except KeyboardInterrupt:
            print("\n[Bridge] 已停止")
        except Exception as e:
            print(f"[Bridge] WebSocket 错误: {e}")
            import traceback
            traceback.print_exc()
    finally:
        release_single_instance(lock_result)


if __name__ == "__main__":
    main()
