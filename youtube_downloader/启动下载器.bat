@echo off
chcp 65001 >nul
title YouTube视频下载器
echo ============================================
echo   YouTube视频下载器
echo   支持1080p/2K/4K画质
echo ============================================
echo.

:: 检查 Python
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未安装 Python!
    echo 请访问 https://www.python.org/downloads/ 安装 Python
    pause
    exit /b 1
)

:: 检查 yt-dlp
python -c "import yt_dlp" >nul 2>&1
if errorlevel 1 (
    echo 正在安装 yt-dlp...
    python -m pip install -U yt-dlp
)

:: 检查 ffmpeg
ffmpeg -version >nul 2>&1
if errorlevel 1 (
    echo 警告: 未安装 ffmpeg，音视频合并将无法正常工作
    echo 请运行: choco install ffmpeg
    echo.
)

:: 启动 GUI
cscript //NoLogo "%~dp0YouTubeDownloader.vbs"

echo.
echo 窗口将在3秒后关闭...
timeout /t 3 /nobreak >nul
