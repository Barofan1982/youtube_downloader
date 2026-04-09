#!/usr/bin/env python3
"""
YouTube视频下载器 - CLI版本 (供VBS GUI调用)
支持1080p以上画质下载并合并音频
"""

import os
import sys
import re
import subprocess
import argparse
from pathlib import Path


def check_ffmpeg():
    """检查ffmpeg是否已安装"""
    try:
        subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("错误: 未检测到 ffmpeg!")
        print("请先安装 ffmpeg: https://ffmpeg.org/download.html")
        return False


def validate_youtube_url(url):
    """验证YouTube URL"""
    patterns = [
        r'^https?://(www\.)?youtube\.com/watch\?v=[\w-]+',
        r'^https?://(www\.)?youtube\.com/shorts/[\w-]+',
        r'^https?://youtu\.be/[\w-]+',
        r'^https?://(www\.)?youtube\.com/playlist\?list=[\w-]+',
    ]
    return any(re.match(pattern, url) for pattern in patterns)


def get_output_dir():
    """获取输出目录"""
    output_dir = Path.home() / 'Downloads' / 'YouTube'
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir


def download_video(url, quality='best', output_dir=None):
    """下载YouTube视频"""
    if not validate_youtube_url(url):
        print(f"错误: 无效的YouTube URL: {url}")
        return False

    if output_dir is None:
        output_dir = get_output_dir()
    else:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

    # 根据质量选择格式
    format_map = {
        'best': 'bestvideo[height<=2160][ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio/best',
        '4k': 'bestvideo[height<=2160][ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio/best',
        '2k': 'bestvideo[height<=1440][ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio/best',
        '1080': 'bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio/best',
    }
    video_format = format_map.get(quality, format_map['best'])

    ydl_opts = {
        'format': video_format,
        'outtmpl': str(output_dir / '%(title)s.%(ext)s'),
        'merge_output_format': 'mp4',
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4',
        }],
        'writethumbnail': True,
        'embedthumbnail': True,
        'addmetadata': True,
        'ignoreerrors': True,
        'no_warnings': False,
        'progress_hooks': [lambda d: print(f"\r进度: {d.get('_percent_str', '0%')}", end='', flush=True) if d['status'] == 'downloading' else None],
    }

    print(f"\n{'='*50}")
    print(f"下载视频: {url}")
    print(f"画质: {quality}")
    print(f"输出目录: {output_dir}")
    print(f"{'='*50}\n")

    try:
        import yt_dlp
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            if info:
                title = info.get('title', 'Unknown')
                print(f"\n\n✓ 下载完成: {title}")
        return True
    except Exception as e:
        print(f"\n\n✗ 下载失败: {e}")
        return False


def download_audio_only(url, output_dir=None):
    """仅下载音频（MP3格式）"""
    if not validate_youtube_url(url):
        print(f"错误: 无效的YouTube URL: {url}")
        return False

    if output_dir is None:
        output_dir = get_output_dir()
    else:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': str(output_dir / '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }],
        'ignoreerrors': True,
        'no_warnings': False,
        'progress_hooks': [lambda d: print(f"\r进度: {d.get('_percent_str', '0%')}", end='', flush=True) if d['status'] == 'downloading' else None],
    }

    print(f"\n{'='*50}")
    print(f"下载音频: {url}")
    print(f"输出目录: {output_dir}")
    print(f"{'='*50}\n")

    try:
        import yt_dlp
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print("\n\n✓ 音频下载完成")
        return True
    except Exception as e:
        print(f"\n\n✗ 下载失败: {e}")
        return False


def batch_download(url_file, quality='best'):
    """批量下载"""
    if not os.path.exists(url_file):
        print(f"错误: 找不到文件 {url_file}")
        return

    with open(url_file, 'r', encoding='utf-8') as f:
        urls = [line.strip() for line in f if line.strip()]

    print(f"批量下载 {len(urls)} 个视频...")
    success = 0
    for i, url in enumerate(urls, 1):
        print(f"\n[{i}/{len(urls)}]")
        if download_video(url, quality):
            success += 1

    print(f"\n{'='*50}")
    print(f"完成: {success}/{len(urls)} 个视频下载成功")
    print(f"{'='*50}")


def main():
    parser = argparse.ArgumentParser(description='YouTube视频下载器')
    parser.add_argument('url', nargs='?', help='YouTube视频URL')
    parser.add_argument('quality', nargs='?', default='best', help='画质: best/1080/2k/4k/audio')
    parser.add_argument('--batch', metavar='FILE', help='批量下载模式，从文件读取URL列表')

    args = parser.parse_args()

    if not check_ffmpeg():
        sys.exit(1)

    try:
        import yt_dlp
    except ImportError:
        print("正在安装 yt-dlp...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-U', 'yt-dlp'], check=True)
        import yt_dlp

    if args.batch:
        batch_download(args.batch, 'best')
    elif args.url:
        if args.quality == 'audio':
            download_audio_only(args.url)
        else:
            download_video(args.url, args.quality)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
