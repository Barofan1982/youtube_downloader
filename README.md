# YouTube Video Downloader

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.7%2B-blue)](https://www.python.org/)
[![yt-dlp](https://img.shields.io/badge/yt--dlp-powered-green)](https://github.com/yt-dlp/yt-dlp)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

**A simple yet powerful YouTube video downloader supporting 1080p/2K/4K quality**

[English](#english) | [中文](#中文)

</div>

---

<a name="english"></a>
## 🇺🇸 English

### 📁 Project Structure

```
youtube_downloader/
├── youtube_downloader/           # V1: Feature-rich version
│   ├── YouTubeDownloader.vbs    # VBS GUI launcher
│   ├── youtube_downloader.py    # Interactive Python version
│   ├── youtube_downloader_cli.py # CLI version
│   └── 启动下载器.bat            # Windows batch launcher
│
├── youtube_downloader_v2/        # V2: Simplified version (Recommended)
│   ├── YouTubeDownloader.vbs    # VBS launcher (hides console)
│   ├── gui.py                   # Python tkinter GUI
│   └── README.md
│
└── youtube_downloader_v1_backup/ # V1 backup
```

### 🚀 Quick Start

#### V2 (Recommended) - Simple & Clean

1. **Install dependencies**
   ```bash
   pip install yt-dlp
   # ffmpeg is required for merging audio/video
   # Windows: choco install ffmpeg
   # Mac: brew install ffmpeg
   # Linux: sudo apt install ffmpeg
   ```

2. **Run**
   ```bash
   cd youtube_downloader_v2
   # Double-click YouTubeDownloader.vbs
   # Or run: python gui.py
   ```

**V2 Features:**
- ✅ Auto-detect highest available quality
- ✅ Single-window GUI (tkinter)
- ✅ Built-in progress bar, no popup windows
- ✅ Auto-merge audio/video to MP4
- ✅ Save to user's Downloads folder by default

#### V1 - Feature-rich

```bash
cd youtube_downloader
# VBS GUI: double-click YouTubeDownloader.vbs
# Or CLI: python youtube_downloader_cli.py "URL" 4k
# Or interactive: python youtube_downloader.py
```

**V1 Features:**
- ✅ Multiple quality options (1080p/2K/4K/Best)
- ✅ Batch download support
- ✅ Audio-only download (MP3)
- ✅ VBS GUI, CLI, and interactive modes

### 📋 Requirements

- Windows 7/10/11 (VBS GUI) or any OS (Python CLI)
- Python 3.7+
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- [ffmpeg](https://ffmpeg.org/) (for audio/video merging)

### 🔧 Installation

```bash
# Clone repository
git clone https://github.com/Barofan1982/youtube_downloader.git
cd youtube_downloader

# Install Python dependencies
pip install yt-dlp

# Install ffmpeg (Windows with Chocolatey)
choco install ffmpeg

# Or download from https://ffmpeg.org/download.html
```

### 📖 Usage Examples

**V2 - Simple GUI:**
```bash
# Just double-click YouTubeDownloader.vbs in youtube_downloader_v2 folder
# Paste URL → Click Download → Done
```

**V1 - CLI:**
```bash
# Download 4K video
python youtube_downloader/youtube_downloader_cli.py "https://youtube.com/watch?v=xxx" 4k

# Download audio only
python youtube_downloader/youtube_downloader_cli.py "https://youtube.com/watch?v=xxx" audio

# Batch download from file
python youtube_downloader/youtube_downloader_cli.py --batch urls.txt
```

### 🆚 V1 vs V2 Comparison

| Feature | V1 | V2 (Recommended) |
|---------|-----|------------------|
| Quality selection | Manual (1080p/2K/4K) | Auto (highest available) |
| Interface | Multi-mode (VBS/CLI/Interactive) | Single GUI window |
| Progress display | External windows | Built-in progress bar |
| Complexity | Feature-rich | Simple & clean |
| Best for | Power users | Casual users |

---

<a name="中文"></a>
## 🇨🇳 中文

### 📁 项目结构

```
youtube_downloader/
├── youtube_downloader/           # V1: 功能丰富版本
│   ├── YouTubeDownloader.vbs    # VBS 图形界面启动器
│   ├── youtube_downloader.py    # Python 交互式版本
│   ├── youtube_downloader_cli.py # 命令行版本
│   └── 启动下载器.bat            # Windows 批处理启动
│
├── youtube_downloader_v2/        # V2: 简洁版本（推荐）
│   ├── YouTubeDownloader.vbs    # VBS 启动器（隐藏控制台）
│   ├── gui.py                   # Python tkinter 图形界面
│   └── README.md
│
└── youtube_downloader_v1_backup/ # V1 备份
```

### 🚀 快速开始

#### V2（推荐）- 简洁易用

1. **安装依赖**
   ```bash
   pip install yt-dlp
   # ffmpeg 用于合并音视频
   # Windows: choco install ffmpeg
   # Mac: brew install ffmpeg
   # Linux: sudo apt install ffmpeg
   ```

2. **运行**
   ```bash
   cd youtube_downloader_v2
   # 双击 YouTubeDownloader.vbs
   # 或运行: python gui.py
   ```

**V2 特性:**
- ✅ 自动识别最高可用画质
- ✅ 单窗口图形界面 (tkinter)
- ✅ 内置进度条，无弹窗
- ✅ 自动合并音视频为 MP4
- ✅ 默认保存到用户下载文件夹

#### V1 - 功能丰富

```bash
cd youtube_downloader
# VBS 界面: 双击 YouTubeDownloader.vbs
# 或命令行: python youtube_downloader_cli.py "链接" 4k
# 或交互式: python youtube_downloader.py
```

**V1 特性:**
- ✅ 多画质选择 (1080p/2K/4K/最高)
- ✅ 批量下载支持
- ✅ 仅下载音频 (MP3)
- ✅ VBS 界面、命令行、交互式三种模式

### 📋 系统要求

- Windows 7/10/11（VBS 界面）或任意系统（Python CLI）
- Python 3.7+
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- [ffmpeg](https://ffmpeg.org/)（音视频合并必需）

### 🔧 安装步骤

```bash
# 克隆仓库
git clone https://github.com/Barofan1982/youtube_downloader.git
cd youtube_downloader

# 安装 Python 依赖
pip install yt-dlp

# 安装 ffmpeg（Windows 用 Chocolatey）
choco install ffmpeg

# 或从 https://ffmpeg.org/download.html 下载
```

### 📖 使用示例

**V2 - 简洁图形界面:**
```bash
# 直接双击 youtube_downloader_v2 文件夹中的 YouTubeDownloader.vbs
# 粘贴链接 → 点击下载 → 完成
```

**V1 - 命令行:**
```bash
# 下载 4K 视频
python youtube_downloader/youtube_downloader_cli.py "https://youtube.com/watch?v=xxx" 4k

# 仅下载音频
python youtube_downloader/youtube_downloader_cli.py "https://youtube.com/watch?v=xxx" audio

# 从文件批量下载
python youtube_downloader/youtube_downloader_cli.py --batch urls.txt
```

### 🆚 V1 与 V2 对比

| 功能 | V1 | V2（推荐） |
|------|-----|-----------|
| 画质选择 | 手动 (1080p/2K/4K) | 自动（最高可用） |
| 界面模式 | 多模式 (VBS/CLI/交互式) | 单窗口图形界面 |
| 进度显示 | 外部窗口 | 内置进度条 |
| 复杂度 | 功能丰富 | 简洁易用 |
| 适合用户 | 高级用户 | 普通用户 |

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

欢迎贡献！请随时提交 Pull Request。

## 📝 License

This project is licensed under the MIT License.

本项目采用 MIT 许可证。

## ⚠️ Disclaimer

This tool is for personal use only. Please respect copyright laws and YouTube's Terms of Service.

本工具仅供个人使用。请尊重版权法和 YouTube 服务条款。

---

<div align="center">

**Made with ❤️ by Barofan1982 & Claude**

</div>
