# YouTube Downloader V2

简洁版本 - 自动识别最高分辨率，一键下载。

## 特性

- 粘贴链接，自动下载最高画质
- 自动合并音视频为 MP4
- 内置进度条，无需额外窗口
- 默认保存到用户 Downloads 目录

## 文件说明

| 文件 | 说明 |
|------|------|
| `YouTubeDownloader.vbs` | 启动程序，双击运行 |
| `download.py` | 下载核心（自动调用）|

## 使用方式

1. 双击 `YouTubeDownloader.vbs`
2. 粘贴 YouTube 链接
3. 点击 Download
4. 等待完成

## 依赖

```bash
pip install yt-dlp
```

## 与 V1 区别

| V1 | V2 |
|----|----|
| 多画质选择 | 自动最高画质 |
| 多窗口交互 | 单一窗口内完成 |
| 复杂菜单 | 简洁界面 |
