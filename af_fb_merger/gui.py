#!/usr/bin/env python3
"""
AppsFlyer x Facebook Merger - tkinter GUI
Pick AF + FB exports, merge on campaign / country, export multi-sheet XLSX.
"""
import os
import subprocess
import sys
import threading
import tkinter as tk
from datetime import datetime
from pathlib import Path
from tkinter import filedialog, messagebox, ttk


def _ensure_deps():
    """pip install pandas & openpyxl on first run."""
    try:
        import pandas  # noqa: F401
        import openpyxl  # noqa: F401
    except ImportError:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "pandas", "openpyxl"],
            capture_output=True,
        )


_ensure_deps()

import merger  # noqa: E402  (import after ensuring deps)


DEFAULT_OUTPUT_DIR = Path.home() / "Downloads"


class FilePickerRow:
    """A label + entry + browse-button row for picking one file."""

    def __init__(self, parent, label_text: str, filetypes):
        self.path_var = tk.StringVar()
        self.filetypes = filetypes

        row = ttk.Frame(parent)
        row.pack(fill=tk.X, pady=4)

        ttk.Label(row, text=label_text, width=12, font=("Segoe UI", 10)).pack(side=tk.LEFT)
        self.entry = ttk.Entry(row, textvariable=self.path_var, font=("Segoe UI", 9))
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 6))
        ttk.Button(row, text="浏览...", command=self._browse, width=8).pack(side=tk.LEFT)

    def _browse(self):
        path = filedialog.askopenfilename(filetypes=self.filetypes)
        if path:
            self.path_var.set(path)

    def get(self) -> str:
        return self.path_var.get().strip()


class MergeTab:
    """Shared logic for all merge tabs (campaign / region / country_campaign)."""

    def __init__(self, parent, *, level: str, title: str):
        self.level = level  # 'campaign' | 'region' | 'country_campaign'
        self.title = title

        frame = ttk.Frame(parent, padding=15)
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text=title, font=("Segoe UI", 14, "bold")).pack(anchor=tk.W, pady=(0, 10))

        filetypes = [("表格文件", "*.csv *.xlsx *.xls"), ("所有文件", "*.*")]
        self.af_row = FilePickerRow(frame, "AppsFlyer:", filetypes)
        self.fb_row = FilePickerRow(frame, "Facebook:", filetypes)

        self.export_btn = ttk.Button(frame, text="导出 XLSX", command=self._start_export)
        self.export_btn.pack(fill=tk.X, pady=(12, 8), ipady=6)

        self.progress = ttk.Progressbar(frame, mode="indeterminate")
        self.progress.pack(fill=tk.X, pady=(0, 8))

        self.status_var = tk.StringVar(value="就绪。选择 AF 和 FB 文件后点「导出 XLSX」。")
        ttk.Label(frame, textvariable=self.status_var, font=("Segoe UI", 9),
                  wraplength=520, foreground="#333").pack(anchor=tk.W)

        ttk.Label(frame, text=f"输出目录：{DEFAULT_OUTPUT_DIR}",
                  font=("Segoe UI", 8), foreground="gray").pack(anchor=tk.W, pady=(6, 0))

        self.root = parent.winfo_toplevel()
        self._last_output: Path | None = None

    def _start_export(self):
        af_path = self.af_row.get()
        fb_path = self.fb_row.get()
        if not af_path or not fb_path:
            messagebox.showwarning("提示", "请先选择 AF 和 FB 两个文件")
            return
        if not Path(af_path).exists():
            messagebox.showerror("错误", f"AF 文件不存在：\n{af_path}")
            return
        if not Path(fb_path).exists():
            messagebox.showerror("错误", f"FB 文件不存在：\n{fb_path}")
            return

        self.export_btn.config(state="disabled")
        self.progress.start(10)
        self.status_var.set("正在读取文件...")

        t = threading.Thread(target=self._run, args=(af_path, fb_path), daemon=True)
        t.start()

    def _run(self, af_path: str, fb_path: str):
        try:
            af_df, af_raw = merger.load_af(af_path, level=self.level)
            fb_df, fb_raw = merger.load_fb(fb_path, level=self.level)

            self.root.after(0, lambda: self.status_var.set("正在合并..."))

            if self.level == "campaign":
                merged = merger.merge_campaign(af_df, fb_df)
                out_name = f"af_fb_campaign_{datetime.now():%Y%m%d_%H%M%S}.xlsx"
                out_path = DEFAULT_OUTPUT_DIR / out_name
                merger.export_xlsx(
                    out_path,
                    campaign_merged=merged,
                    raw_af_campaign=af_raw,
                    raw_fb_campaign=fb_raw,
                )
            elif self.level == "region":
                merged = merger.merge_region(af_df, fb_df)
                out_name = f"af_fb_region_{datetime.now():%Y%m%d_%H%M%S}.xlsx"
                out_path = DEFAULT_OUTPUT_DIR / out_name
                merger.export_xlsx(
                    out_path,
                    region_merged=merged,
                    raw_af_region=af_raw,
                    raw_fb_region=fb_raw,
                )
            else:  # country_campaign
                merged_long = merger.merge_country_campaign(af_df, fb_df)
                merged = merger.build_country_pivot(merged_long)
                out_name = f"af_fb_country_campaign_{datetime.now():%Y%m%d_%H%M%S}.xlsx"
                out_path = DEFAULT_OUTPUT_DIR / out_name
                merger.export_xlsx(
                    out_path,
                    country_campaign_pivot=merged,
                    raw_af_country_campaign=af_raw,
                    raw_fb_country_campaign=fb_raw,
                )

            unmatched = (merged["_match_status"] != "matched").sum() if "_match_status" in merged.columns else 0
            total = len(merged)
            self._last_output = out_path
            self.root.after(0, lambda: self._done(out_path, total, unmatched))

        except merger.ColumnNotFoundError as e:
            self.root.after(0, lambda msg=str(e): self._error("列名识别失败", msg))
        except Exception as e:
            self.root.after(0, lambda msg=str(e): self._error("导出失败", msg))

    def _done(self, out_path: Path, total: int, unmatched: int):
        self.progress.stop()
        self.export_btn.config(state="normal")
        msg = f"完成：{total} 行，未匹配 {unmatched} 行（已标红）\n→ {out_path}"
        self.status_var.set(msg)
        if messagebox.askyesno("完成", f"{msg}\n\n打开所在文件夹？"):
            self._open_folder(out_path.parent)

    def _error(self, title: str, msg: str):
        self.progress.stop()
        self.export_btn.config(state="normal")
        self.status_var.set(f"错误：{msg}")
        messagebox.showerror(title, msg)

    @staticmethod
    def _open_folder(path: Path):
        if os.name == "nt":
            os.startfile(str(path))  # type: ignore[attr-defined]
        elif sys.platform == "darwin":
            subprocess.run(["open", str(path)])
        else:
            subprocess.run(["xdg-open", str(path)])


class App:
    def __init__(self, root: tk.Tk):
        self.root = root
        root.title("AF x FB Merger")
        root.geometry("640x420")
        root.resizable(False, False)

        root.update_idletasks()
        x = (root.winfo_screenwidth() - 640) // 2
        y = (root.winfo_screenheight() - 420) // 2
        root.geometry(f"+{x}+{y}")

        notebook = ttk.Notebook(root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        campaign_frame = ttk.Frame(notebook)
        region_frame = ttk.Frame(notebook)
        country_campaign_frame = ttk.Frame(notebook)
        notebook.add(campaign_frame, text="Campaign 合并")
        notebook.add(region_frame, text="地区合并")
        notebook.add(country_campaign_frame, text="国家×系列透视")

        MergeTab(campaign_frame, level="campaign", title="Campaign 维度合并")
        MergeTab(region_frame, level="region", title="地区维度合并")
        MergeTab(country_campaign_frame, level="country_campaign",
                 title="国家 × 系统 × 优化目标 × Campaign 透视")


def main():
    if os.name == "nt":
        import ctypes
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

    root = tk.Tk()
    App(root)
    root.mainloop()


if __name__ == "__main__":
    main()
