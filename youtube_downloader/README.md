# YouTube视频下载器

支持1080p/2K/4K画质下载的YouTube视频下载工具，自动合并音视频。

## 功能特点

- 支持多种画质：1080p / 2K / 4K / 最高可用
- 自动合并音视频（使用 ffmpeg）
- 批量下载支持
- 音频单独下载（MP3格式）
- 嵌入视频缩略图和元数据

## 文件说明

| 文件 | 说明 |
|------|------|
| `YouTubeDownloader.vbs` | VBS图形界面，双击运行 |
| `启动下载器.bat` | Windows批处理启动文件 |
| `youtube_downloader_cli.py` | 命令行版本，供VBS调用 |
| `youtube_downloader.py` | 交互式Python脚本 |

## 使用方式

### 方式一：VBS图形界面（推荐）

双击运行 `YouTubeDownloader.vbs` 或 `启动下载器.bat`

### 方式二：命令行

```bash
# 下载最高画质
python youtube_downloader_cli.py "https://youtube.com/watch?v=xxx" best

# 下载4K
python youtube_downloader_cli.py "https://youtube.com/watch?v=xxx" 4k

# 下载音频
python youtube_downloader_cli.py "https://youtube.com/watch?v=xxx" audio

# 批量下载
python youtube_downloader_cli.py --batch urls.txt
```

### 方式三：交互式

```bash
python youtube_downloader.py
```

## 依赖安装

### 必需依赖

```bash
# yt-dlp
pip install yt-dlp

# ffmpeg（必须，用于合并音视频）
choco install ffmpeg
```

### 下载位置

下载的视频默认保存到：`%USERPROFILE%\Downloads\YouTube\`

## 支持的URL格式

- `https://youtube.com/watch?v=xxxxx`
- `https://youtu.be/xxxxx`
- `https://youtube.com/shorts/xxxxx`
- `https://youtube.com/playlist?list=xxxxx`

## 系统要求

- Windows 7/10/11
- Python 3.7+
- ffmpeg 4.0+

## 许可证

MIT License
