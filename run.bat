@echo off
chcp 65001 >nul 2>&1
title Feishu-OpenCode Bridge

cd /d "%~dp0"

echo ==========================================
echo   Feishu ^<^-^> OpenCode Bridge
echo ==========================================
echo.

:: 检查 Python 是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未找到 Python，请先安装 Python 3.x
    echo 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)

:: 检查配置文件
if not exist config.py (
    echo 错误: 配置文件 config.py 不存在！
    echo 请先复制 config.py.example 为 config.py 并填写配置
    echo.
    echo 按任意键退出...
    pause >nul
    exit /b 1
)

:: 运行 Bridge
python bridge.py
if errorlevel 1 (
    echo.
    echo Bridge 启动失败！
    pause
)
