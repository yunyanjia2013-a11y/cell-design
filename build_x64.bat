@echo off
chcp 65001 >nul
echo ============================================
echo   圆柱锂电池极片设计工具 - x64 构建脚本
echo ============================================
echo.

:: Check Python
echo [1/4] 检查 Python x64 环境...
python --version 2>nul
if %errorlevel% neq 0 (
    echo [错误] 未找到 Python，请先安装 Python 3.12 x64 版本
    echo        下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)

:: Verify x64 architecture
python -c "import struct; exit(0 if struct.calcsize('P')==8 else 1)"
if %errorlevel% neq 0 (
    echo [错误] Python 必须是 64 位版本（x64），当前是 32 位
    pause
    exit /b 1
)
echo        Python x64 环境 ✓

:: Install/upgrade pip
echo.
echo [2/4] 安装构建依赖...
python -m pip install --upgrade pip -q
python -m pip install pyinstaller numpy openpyxl -q
if %errorlevel% neq 0 (
    echo [错误] 依赖安装失败
    pause
    exit /b 1
)
echo        依赖安装完成 ✓

:: Clean old build
echo.
echo [3/4] 清理旧构建文件...
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"
echo        清理完成 ✓

:: Build
echo.
echo [4/4] PyInstaller 构建中（需要 1-3 分钟）...
python -m PyInstaller --clean ^
    --name "Electrode_Design" ^
    --onefile ^
    --windowed ^
    --add-data "core;core" ^
    --hidden-import "core.electrode_calc" ^
    --hidden-import "core.material_db" ^
    --hidden-import "openpyxl" ^
    --noupx ^
    --target-architecture x64 ^
    main.py

if %errorlevel% neq 0 (
    echo [错误] 构建失败，请检查上方输出
    pause
    exit /b 1
)

echo.
echo ============================================
echo   构建成功！
echo   输出文件: dist\Electrode_Design.exe
echo.
echo   文件大小:
dir "dist\Electrode_Design.exe" 2>nul
echo ============================================
pause
