#!/usr/bin/env python3
"""
YouTube Downloader V2 - tkinter GUI
Auto-detect highest quality, merge to MP4
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import os
import sys
import re
import subprocess
import threading
import traceback
from pathlib import Path


class DownloaderApp:
    QUALITY_OPTIONS = {
        "720p": "bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/bestvideo[height<=720]+bestaudio/best[height<=720]/best",
        "1080p": "bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/bestvideo[height<=1080]+bestaudio/best[height<=1080]/best",
        "1440p / 2K": "bestvideo[height<=1440][ext=mp4]+bestaudio[ext=m4a]/bestvideo[height<=1440]+bestaudio/best[height<=1440]/best",
        "2160p / 4K": "bestvideo[height<=2160][ext=mp4]+bestaudio[ext=m4a]/bestvideo[height<=2160]+bestaudio/best[height<=2160]/best",
        "Best Available": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio/best",
    }

    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Downloader")
        self.root.geometry("620x430")
        self.root.minsize(560, 380)

        # Center window
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() - 620) // 2
        y = (self.root.winfo_screenheight() - 430) // 2
        self.root.geometry(f"+{x}+{y}")

        self.setup_ui()
        self.check_deps()

    def setup_ui(self):
        # Main frame
        frame = ttk.Frame(self.root, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)

        # Title
        title = ttk.Label(frame, text="YouTube Downloader",
                         font=("Segoe UI", 18, "bold"), foreground="#cc0000")
        title.pack(pady=(0, 15))

        # URL input
        ttk.Label(frame, text="Video URL:", font=("Segoe UI", 10)).pack(anchor=tk.W)
        self.url_var = tk.StringVar()
        self.url_entry = ttk.Entry(frame, textvariable=self.url_var, font=("Segoe UI", 11))
        self.url_entry.pack(fill=tk.X, pady=(5, 10), ipady=5)
        self.url_entry.focus()

        # Quality selection
        quality_frame = ttk.Frame(frame)
        quality_frame.pack(fill=tk.X, pady=(0, 10))
        ttk.Label(quality_frame, text="Quality:", font=("Segoe UI", 10)).pack(side=tk.LEFT)
        self.quality_var = tk.StringVar(value="1080p")
        self.quality_combo = ttk.Combobox(
            quality_frame,
            textvariable=self.quality_var,
            values=list(self.QUALITY_OPTIONS.keys()),
            state="readonly",
            width=16,
        )
        self.quality_combo.pack(side=tk.LEFT, padx=(8, 0))

        # Download button
        self.btn = ttk.Button(frame, text="Download", command=self.start_download)
        self.btn.pack(fill=tk.X, pady=(5, 10), ipady=8)

        # Progress bar
        self.progress = ttk.Progressbar(frame, mode='determinate', maximum=100)
        self.progress.pack(fill=tk.X, pady=(5, 10))

        # Log area
        ttk.Label(frame, text="Status:", font=("Segoe UI", 10)).pack(anchor=tk.W, pady=(4, 4))
        self.log = scrolledtext.ScrolledText(
            frame,
            height=7,
            wrap=tk.WORD,
            font=("Consolas", 9),
            state=tk.DISABLED,
        )
        self.log.pack(fill=tk.BOTH, expand=True)
        self.set_status("Ready. Paste URL and click Download.")

        # Output path
        self.output_dir = Path.home() / "Downloads"
        ttk.Label(frame, text=f"Save to: {self.output_dir}",
                 font=("Segoe UI", 8), foreground="gray").pack(anchor=tk.W, pady=(10, 0))

    def check_deps(self):
        """Check ffmpeg and yt-dlp"""
        try:
            subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
        except:
            self.set_status("Warning: ffmpeg not found. Please install ffmpeg.")

        try:
            import yt_dlp
        except ImportError:
            self.set_status("Installing yt-dlp...")
            self.root.update()
            subprocess.run([sys.executable, '-m', 'pip', 'install', '-U', 'yt-dlp'],
                          capture_output=True)

    def validate_url(self, url):
        return 'youtube.com' in url or 'youtu.be' in url

    def start_download(self):
        url = self.url_var.get().strip()

        if not url:
            messagebox.showwarning("Warning", "Please enter a URL")
            return

        if not self.validate_url(url):
            messagebox.showwarning("Warning", "Invalid YouTube URL")
            return

        self.btn.config(state='disabled')
        self.progress['value'] = 0
        quality = self.quality_var.get()
        self.set_status(f"Starting download... Quality limit: {quality}")

        # Run download in thread
        thread = threading.Thread(target=self.download, args=(url, quality))
        thread.daemon = True
        thread.start()

    def download(self, url, quality):
        """Download with yt-dlp"""
        try:
            from yt_dlp import YoutubeDL

            self.output_dir.mkdir(parents=True, exist_ok=True)

            def progress_hook(d):
                if d['status'] == 'downloading':
                    pct_str = d.get('_percent_str', '0%').strip().replace('%', '')
                    try:
                        pct = float(pct_str)
                    except:
                        pct = 0
                    speed = d.get('_speed_str', 'N/A')
                    eta = d.get('_eta_str', 'N/A')

                    self.root.after(0, lambda: self.update_progress(pct, f"Downloading: {pct:.1f}% | Speed: {speed} | ETA: {eta}"))

                elif d['status'] == 'finished':
                    self.root.after(0, lambda: self.set_status("Download finished, merging audio/video..."))

            ydl_opts = {
                'format': self.QUALITY_OPTIONS[quality],
                'outtmpl': str(self.output_dir / '%(title)s.%(ext)s'),
                'merge_output_format': 'mp4',
                'postprocessors': [{
                    'key': 'FFmpegVideoConvertor',
                    'preferedformat': 'mp4',
                }],
                'progress_hooks': [progress_hook],
                'quiet': True,
                'no_warnings': True,
            }

            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                title = info.get('title', 'Unknown')

            self.root.after(0, lambda: self.download_complete(title))

        except Exception as e:
            self.root.after(0, lambda: self.download_error(str(e)))

    def update_progress(self, value, msg):
        self.progress['value'] = value
        self.set_status(msg)

    def download_complete(self, title):
        self.progress['value'] = 100
        self.set_status(f"Complete: {title}")
        self.btn.config(state='normal')
        messagebox.showinfo("Success", f"Download complete!\n\nSaved to: {self.output_dir}")

    def download_error(self, error):
        self.set_status(f"Error: {error}")
        self.btn.config(state='normal')
        messagebox.showerror("Error", f"Download failed:\n{error}")

    def set_status(self, msg):
        self.log.config(state=tk.NORMAL)
        self.log.insert(tk.END, msg + "\n")
        self.log.see(tk.END)
        self.log.config(state=tk.DISABLED)


def main():
    # Hide console window on Windows
    if os.name == 'nt':
        import ctypes
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

    root = tk.Tk()
    app = DownloaderApp(root)
    root.mainloop()


if __name__ == '__main__':
    try:
        main()
    except Exception:
        log_path = Path(__file__).with_name('youtube_downloader_v2_error.log')
        log_path.write_text(traceback.format_exc(), encoding='utf-8')
        raise
