"""
FileSort Pro - Windows System Tray App
Watches Downloads folder and auto-sorts files
"""

import os
import sys
import shutil
import json
import threading
import time
import winreg
from pathlib import Path
from datetime import datetime

import pystray
from pystray import MenuItem as item
from PIL import Image, ImageDraw
import win11toast
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# ── Config paths ──────────────────────────────────────────────────
HOME         = Path.home()
DOWNLOADS    = HOME / "Downloads"
CONFIG_FILE  = HOME / "AppData" / "Roaming" / "FileSortPro" / "config.json"
LOG_FILE     = HOME / "AppData" / "Roaming" / "FileSortPro" / "activity.log"
CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)

# ── Default sorting rules ─────────────────────────────────────────
DEFAULT_RULES = [
    {"name": "CV / Resume",      "pattern": r"(?i)(CV|resume|curriculum)",      "folder": str(HOME / "Shahid_Ali_Documents" / "CV_Versions"),             "icon": "📄"},
    {"name": "Cover Letter",     "pattern": r"(?i)cover.?letter",               "folder": str(HOME / "Shahid_Ali_Documents" / "Cover_Letters"),           "icon": "✉️"},
    {"name": "SOP",              "pattern": r"(?i)SOP",                          "folder": str(HOME / "Shahid_Ali_Documents" / "Scholarship_Applications"), "icon": "📋"},
    {"name": "LOR",              "pattern": r"(?i)LOR",                          "folder": str(HOME / "Shahid_Ali_Documents" / "Scholarship_Applications"), "icon": "📜"},
    {"name": "Invoice",          "pattern": r"(?i)(invoice|receipt)",            "folder": str(HOME / "Shahid_Ali_Documents" / "Invoices"),                "icon": "🧾"},
    {"name": "Images",           "ext": ["jpg","jpeg","png","gif","webp","jfif"],"folder": str(HOME / "Downloads_Sorted" / "Images"),                     "icon": "🖼️"},
    {"name": "Videos",           "ext": ["mp4","mov","avi","mkv"],               "folder": str(HOME / "Downloads_Sorted" / "Videos"),                     "icon": "🎬"},
    {"name": "Music",            "ext": ["mp3","wav","flac","aac"],              "folder": str(HOME / "Downloads_Sorted" / "Music"),                      "icon": "🎵"},
    {"name": "PDF Documents",    "ext": ["pdf"],                                 "folder": str(HOME / "Downloads_Sorted" / "PDFs"),                       "icon": "📕"},
    {"name": "Word Documents",   "ext": ["doc","docx"],                          "folder": str(HOME / "Shahid_Ali_Documents" / "Personal_Documents"),     "icon": "📝"},
    {"name": "Spreadsheets",     "ext": ["xls","xlsx","csv"],                    "folder": str(HOME / "Shahid_Ali_Documents" / "Personal_Documents"),     "icon": "📊"},
    {"name": "Archives",         "ext": ["zip","rar","7z","tar","gz"],           "folder": str(HOME / "Downloads_Sorted" / "Archives"),                   "icon": "📦"},
    {"name": "Presentations",    "ext": ["ppt","pptx"],                          "folder": str(HOME / "Shahid_Ali_Documents" / "Personal_Documents"),     "icon": "📽️"},
    {"name": "Code Files",       "ext": ["js","py","html","css","ts","json"],    "folder": str(HOME / "Downloads_Sorted" / "Code"),                       "icon": "💻"},
    {"name": "Installers",       "ext": ["exe","msi","dmg","pkg"],               "folder": str(HOME / "Downloads_Sorted" / "Installers"),                 "icon": "⚙️"},
]

# ── Load / save config ────────────────────────────────────────────
def load_config():
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE) as f:
            return json.load(f)
    return {"enabled": True, "rules": DEFAULT_RULES, "sorted_count": 0}

def save_config(cfg):
    with open(CONFIG_FILE, "w") as f:
        json.dump(cfg, f, indent=2)

config = load_config()

# ── Log activity ──────────────────────────────────────────────────
def log_activity(msg):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}\n")

# ── Match file to rule ────────────────────────────────────────────
import re

def match_rule(filename):
    name = filename.lower()
    ext  = Path(filename).suffix.lstrip(".").lower()
    for rule in config["rules"]:
        if "pattern" in rule and re.search(rule["pattern"], name):
            return rule
        if "ext" in rule and ext in rule["ext"]:
            return rule
    return None

# ── Move file safely ──────────────────────────────────────────────
def move_file_safe(src, dest_folder):
    dest = Path(dest_folder)
    dest.mkdir(parents=True, exist_ok=True)
    dest_file = dest / Path(src).name
    if dest_file.exists():
        stem = Path(src).stem
        suf  = Path(src).suffix
        dest_file = dest / f"{stem}_{int(time.time())}{suf}"
    shutil.move(str(src), str(dest_file))
    return dest_file

# ── File watcher ──────────────────────────────────────────────────
class DownloadHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        time.sleep(1.5)  # wait for download to complete
        if not config.get("enabled", True):
            return
        filepath = Path(event.src_path)
        if not filepath.exists():
            return
        rule = match_rule(filepath.name)
        if not rule:
            return
        try:
            dest = move_file_safe(filepath, rule["folder"])
            config["sorted_count"] = config.get("sorted_count", 0) + 1
            save_config(config)
            msg = f"{rule['icon']} {filepath.name} → {rule['name']}"
            log_activity(msg)
            # Windows toast notification
            try:
                win11toast.notify(
                    "FileSort Pro",
                    f"{filepath.name}\n→ {rule['name']}",
                    app_id="FileSort Pro",
                    duration="short"
                )
            except:
                pass
            # Update tray tooltip
            update_tray()
        except Exception as e:
            log_activity(f"ERROR: {e}")

observer = Observer()
observer.schedule(DownloadHandler(), str(DOWNLOADS), recursive=False)

# ── Tray icon ─────────────────────────────────────────────────────
def create_tray_icon():
    img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    d   = ImageDraw.Draw(img)
    d.rounded_rectangle([4, 4, 60, 60], radius=14, fill=(108, 99, 255, 255))
    d.rectangle([16, 24, 48, 44], fill=(255, 255, 255, 200))
    d.line([22, 32, 42, 32], fill=(108, 99, 255, 255), width=3)
    d.line([22, 38, 36, 38], fill=(108, 99, 255, 255), width=3)
    return img

tray_icon = None

def update_tray():
    global tray_icon
    if tray_icon:
        count = config.get("sorted_count", 0)
        tray_icon.title = f"FileSort Pro — {count} files sorted"

def toggle_enabled(icon, item):
    config["enabled"] = not config["enabled"]
    save_config(config)
    update_tray()

def open_log(icon, item):
    os.startfile(str(LOG_FILE))

def open_downloads(icon, item):
    os.startfile(str(DOWNLOADS))

def add_to_startup():
    key = winreg.OpenKey(
        winreg.HKEY_CURRENT_USER,
        r"Software\Microsoft\Windows\CurrentVersion\Run",
        0, winreg.KEY_SET_VALUE
    )
    winreg.SetValueEx(key, "FileSortPro", 0, winreg.REG_SZ, f'"{sys.executable}" "{__file__}"')
    winreg.CloseKey(key)

def remove_from_startup():
    try:
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Run",
            0, winreg.KEY_SET_VALUE
        )
        winreg.DeleteValue(key, "FileSortPro")
        winreg.CloseKey(key)
    except:
        pass

def quit_app(icon, item):
    observer.stop()
    remove_from_startup()
    icon.stop()

def run_tray():
    global tray_icon
    count = config.get("sorted_count", 0)
    menu = pystray.Menu(
        item("FileSort Pro", lambda i, it: None, enabled=False),
        pystray.Menu.SEPARATOR,
        item(lambda text: "Pause sorting" if config.get("enabled") else "Resume sorting", toggle_enabled),
        item("Open Downloads folder", open_downloads),
        item("View activity log", open_log),
        pystray.Menu.SEPARATOR,
        item("Quit", quit_app),
    )
    tray_icon = pystray.Icon(
        "FileSortPro",
        create_tray_icon(),
        f"FileSort Pro — {count} files sorted",
        menu
    )
    tray_icon.run()

# ── Main ──────────────────────────────────────────────────────────
if __name__ == "__main__":
    add_to_startup()
    observer.start()
    log_activity("FileSort Pro started")
    try:
        win11toast.notify("FileSort Pro", "Running in system tray!\nYour downloads will be sorted automatically.", app_id="FileSort Pro")
    except:
        pass
    run_tray()
