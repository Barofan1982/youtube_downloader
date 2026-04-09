# YouTube Downloader V2

Simple GUI downloader with auto quality detection.

## Files

| File | Purpose |
|------|---------|
| `YouTubeDownloader.vbs` | Launcher - double click to run |
| `gui.py` | Main application (auto-launched) |

## Usage

1. Double click `YouTubeDownloader.vbs`
2. Paste YouTube URL
3. Click Download
4. Wait for completion

## Features

- Auto-detect highest available quality
- Auto-merge audio/video to MP4
- Built-in progress bar (no popup windows)
- Save to user's Downloads folder by default

## Requirements

```bash
pip install yt-dlp
```

ffmpeg must be installed (for audio/video merging).

## VS V1

| V1 | V2 |
|----|----|
| Multiple quality options | Auto highest quality |
| Multiple windows/popups | Single window |
| VBS+HTML+JS mix | Python tkinter GUI |
| Complex code | Simple and clean |
