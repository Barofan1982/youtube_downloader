#!/usr/bin/env python3
"""
YouTube视频下载器
支持1080p以上画质下载，自动合并音视频
"""

import os
import sys
import re
import subprocess
from pathlib import Path
from urllib.parse import urlparse


def check_ffmpeg():
    """检查ffmpeg是否已安装"""
    try:
        subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def install_yt_dlp():
    """安装yt-dlp"""
    try:
        import yt_dlp
        return True
    except ImportError:
        print("正在安装 yt-dlp...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-U', 'yt-dlp'], check=True)
        return True


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
    """
    下载YouTube视频

    Args:
        url: YouTube视频URL
        quality: 画质选择 ('best', '1080', '2k', '4k')
        output_dir: 输出目录
    """
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
        'extractaudio': False,
        'keepvideo': True,
    }

    # 添加cookies处理（如果需要）
    cookie_file = Path.home() / '.youtube_cookies.txt'
    if cookie_file.exists():
        ydl_opts['cookiefile'] = str(cookie_file)

    print(f"\n{'='*50}")
    print(f"下载视频: {url}")
    print(f"画质设置: {quality}")
    print(f"输出目录: {output_dir}")
    print(f"{'='*50}\n")

    try:
        import yt_dlp
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            if info:
                title = info.get('title', 'Unknown')
                duration = info.get('duration', 0)
                duration_str = f"{duration//60}:{duration%60:02d}" if duration else "Unknown"
                print(f"\n✓ 下载完成: {title}")
                print(f"  时长: {duration_str}")
        return True
    except Exception as e:
        print(f"\n✗ 下载失败: {e}")
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
    }

    print(f"\n{'='*50}")
    print(f"下载音频: {url}")
    print(f"输出目录: {output_dir}")
    print(f"{'='*50}\n")

    try:
        import yt_dlp
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print("\n✓ 音频下载完成")
        return True
    except Exception as e:
        print(f"\n✗ 下载失败: {e}")
        return False


def main():
    """主函数"""
    print("="*50)
    print("YouTube视频下载器")
    print("支持1080p/2K/4K画质 | 自动合并音视频")
    print("="*50)

    # 检查依赖
    if not check_ffmpeg():
        print("\n警告: 未检测到 ffmpeg!")
        print("请安装 ffmpeg 后再使用:")
        print("  Windows: choco install ffmpeg")
        print("  Mac: brew install ffmpeg")
        print("  Linux: sudo apt install ffmpeg")
        print("\n或者访问: https://ffmpeg.org/download.html")
        return

    if not install_yt_dlp():
        print("无法安装 yt-dlp，请手动安装: pip install yt-dlp")
        return

    # 交互式菜单
    while True:
        print("\n请选择操作:")
        print("1. 下载视频 (最高画质)")
        print("2. 下载视频 (1080p)")
        print("3. 下载视频 (2K)")
        print("4. 下载视频 (4K)")
        print("5. 仅下载音频 (MP3)")
        print("6. 批量下载视频")
        print("0. 退出")

        choice = input("\n请输入选项 (0-6): ").strip()

        if choice == '0':
            print("再见!")
            break

        elif choice in ['1', '2', '3', '4']:
            url = input("请输入YouTube视频URL: ").strip()
            quality_map = {'1': 'best', '2': '1080', '3': '2k', '4': '4k'}
            download_video(url, quality_map[choice])

        elif choice == '5':
            url = input("请输入YouTube视频URL: ").strip()
            download_audio_only(url)

        elif choice == '6':
            print("请输入多个YouTube URL，每行一个，输入空行结束:")
            urls = []
            while True:
                url = input().strip()
                if not url:
                    break
                urls.append(url)

            if urls:
                print(f"\n开始批量下载 {len(urls)} 个视频...")
                success = 0
                for i, url in enumerate(urls, 1):
                    print(f"\n[{i}/{len(urls)}]")
                    if download_video(url):
                        success += 1
                print(f"\n✓ 完成: {success}/{len(urls)} 个视频下载成功")

        else:
            print("无效选项，请重新输入")


if __name__ == '__main__':
    main()
