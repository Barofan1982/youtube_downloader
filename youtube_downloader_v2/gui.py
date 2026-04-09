#!/usr/bin/env python3
"""
YouTube Downloader V2 - tkinter GUI
Auto-detect highest quality, merge to MP4
"""

import tkinter as tk
from tkinter import ttk, messagebox
import os
import sys
import re
import subprocess
import threading
from pathlib import Path


class DownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Downloader")
        self.root.geometry("500x280")
        self.root.resizable(False, False)

        # Center window
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() - 500) // 2
        y = (self.root.winfo_screenheight() - 280) // 2
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

        # Download button
        self.btn = ttk.Button(frame, text="Download", command=self.start_download)
        self.btn.pack(fill=tk.X, pady=(5, 10), ipady=8)

        # Progress bar
        self.progress = ttk.Progressbar(frame, mode='determinate', maximum=100)
        self.progress.pack(fill=tk.X, pady=(5, 10))

        # Status label
        self.status_var = tk.StringVar(value="Ready. Paste URL and click Download.")
        self.status = ttk.Label(frame, textvariable=self.status_var,
                               font=("Segoe UI", 9), wraplength=460)
        self.status.pack(anchor=tk.W)

        # Output path
        self.output_dir = Path.home() / "Downloads"
        ttk.Label(frame, text=f"Save to: {self.output_dir}",
                 font=("Segoe UI", 8), foreground="gray").pack(anchor=tk.W, pady=(10, 0))

    def check_deps(self):
        """Check ffmpeg and yt-dlp"""
        try:
            subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
        except:
            self.status_var.set("Warning: ffmpeg not found. Please install ffmpeg.")

        try:
            import yt_dlp
        except ImportError:
            self.status_var.set("Installing yt-dlp...")
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
        self.status_var.set("Starting...")

        # Run download in thread
        thread = threading.Thread(target=self.download, args=(url,))
        thread.daemon = True
        thread.start()

    def download(self, url):
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
                    self.root.after(0, lambda: self.status_var.set("Download finished, merging audio/video..."))

            ydl_opts = {
                'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
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
        self.status_var.set(msg)

    def download_complete(self, title):
        self.progress['value'] = 100
        self.status_var.set(f"Complete: {title}")
        self.btn.config(state='normal')
        messagebox.showinfo("Success", f"Download complete!\n\nSaved to: {self.output_dir}")

    def download_error(self, error):
        self.status_var.set(f"Error: {error}")
        self.btn.config(state='normal')
        messagebox.showerror("Error", f"Download failed:\n{error}")


def main():
    # Hide console window on Windows
    if os.name == 'nt':
        import ctypes
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

    root = tk.Tk()
    app = DownloaderApp(root)
    root.mainloop()


if __name__ == '__main__':
    main()
