@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo ==========================================
echo   电芯设计 Web 版
echo   与 PC 版共用 core/ 引擎，100%% 一致
echo ==========================================
echo.
echo   浏览器打开: http://127.0.0.1:5555
echo   手机访问:   http://你的电脑IP:5555
echo.
call "C:\Users\JYY_2\AppData\Local\Programs\Python\Python312-arm64\python.exe" app.py
pause
