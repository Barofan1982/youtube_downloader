#!/usr/bin/env python3
"""
YouTube Downloader V2 - Simple & Clean
Auto-detect highest quality, auto-merge to MP4
"""

import sys
import os
import json
from pathlib import Path
from urllib.parse import urlparse

def log(msg, progress_file):
    """Write log to file for GUI to read"""
    with open(progress_file, 'a', encoding='utf-8') as f:
        f.write(msg + '\n')

def is_valid_url(url):
    """Check if URL is valid YouTube link"""
    return 'youtube.com' in url or 'youtu.be' in url

def get_downloads_dir():
    """Get user's Downloads folder"""
    return Path.home() / 'Downloads'

def download(url, progress_file):
    """Download video with auto quality detection"""
    try:
        import yt_dlp
    except ImportError:
        log("ERROR: yt-dlp not installed. Run: pip install yt-dlp", progress_file)
        return False

    if not is_valid_url(url):
        log("ERROR: Invalid YouTube URL", progress_file)
        return False

    output_dir = get_downloads_dir()
    output_dir.mkdir(parents=True, exist_ok=True)

    log(f"Output: {output_dir}", progress_file)
    log("Analyzing video...", progress_file)

    # Progress hook
    def progress_hook(d):
        if d['status'] == 'downloading':
            pct = d.get('_percent_str', '0%').strip()
            speed = d.get('_speed_str', 'N/A')
            eta = d.get('_eta_str', 'N/A')
            log(f"PROGRESS:{pct}|{speed}|{eta}", progress_file)
        elif d['status'] == 'finished':
            log("Download finished, merging...", progress_file)

    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': str(output_dir / '%(title)s.%(ext)s'),
        'merge_output_format': 'mp4',
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4',
        }],
        'progress_hooks': [progress_hook],
        'quiet': True,
        'no_warnings': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            title = info.get('title', 'Unknown')
            resolution = info.get('resolution', 'Unknown')
            log(f"DONE:{title}", progress_file)
            return True
    except Exception as e:
        log(f"ERROR:{str(e)}", progress_file)
        return False

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: download.py <URL> <progress_file>")
        sys.exit(1)

    url = sys.argv[1]
    progress_file = sys.argv[2]

    # Clear progress file
    open(progress_file, 'w').close()

    download(url, progress_file)
