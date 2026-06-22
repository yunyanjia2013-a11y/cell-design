@echo off
chcp 65001 >nul
title 圆柱锂电池极片设计 v4.0

:: Check if Python x64 is available
python --version 2>nul
if %errorlevel% neq 0 (
    echo [错误] 未找到 Python，请先安装 Python 3.12 x64
    echo        下载: https://www.python.org/downloads/
    pause
    exit /b 1
)

:: Install dependencies if needed
python -c "import openpyxl" 2>nul
if %errorlevel% neq 0 (
    echo 正在安装 openpyxl...
    python -m pip install openpyxl -q
)

:: Run the app
python main.py
