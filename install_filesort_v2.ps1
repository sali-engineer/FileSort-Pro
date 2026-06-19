Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force

Clear-Host
Write-Host "========================================" -ForegroundColor Magenta
Write-Host "   FileSort Pro - Reinstall v2          " -ForegroundColor White
Write-Host "========================================" -ForegroundColor Magenta

$installDir = "$env:APPDATA\FileSortPro"
New-Item -ItemType Directory -Path $installDir -Force | Out-Null

# Stop old instance
Get-Process pythonw -ErrorAction SilentlyContinue | Stop-Process -Force
Start-Sleep -Seconds 2

$trayScript = @'
import os, sys, shutil, json, re, time
from pathlib import Path
from datetime import datetime
import pystray
from pystray import MenuItem as item
from PIL import Image, ImageDraw
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

HOME      = Path.home()
DOWNLOADS = HOME / "Downloads"
CFG_DIR   = HOME / "AppData" / "Roaming" / "FileSortPro"
CFG_FILE  = CFG_DIR / "config.json"
LOG_FILE  = CFG_DIR / "activity.log"
CFG_DIR.mkdir(parents=True, exist_ok=True)

RULES = [
    {"name":"CV / Resume",   "pattern":r"(?i)(CV|resume|curriculum)", "folder":str(HOME/"Downloads_Sorted"/"CVs")},
    {"name":"Cover Letter",  "pattern":r"(?i)cover.?letter",          "folder":str(HOME/"Downloads_Sorted"/"Cover_Letters")},
    {"name":"Invoice",       "pattern":r"(?i)(invoice|receipt)",      "folder":str(HOME/"Downloads_Sorted"/"Invoices")},
    {"name":"Images",        "ext":["jpg","jpeg","png","gif","webp","jfif"], "folder":str(HOME/"Downloads_Sorted"/"Images")},
    {"name":"Videos",        "ext":["mp4","mov","avi","mkv"],         "folder":str(HOME/"Downloads_Sorted"/"Videos")},
    {"name":"Music",         "ext":["mp3","wav","flac","aac"],        "folder":str(HOME/"Downloads_Sorted"/"Music")},
    {"name":"PDFs",          "ext":["pdf"],                           "folder":str(HOME/"Downloads_Sorted"/"PDFs")},
    {"name":"Word Docs",     "ext":["doc","docx"],                    "folder":str(HOME/"Downloads_Sorted"/"Documents")},
    {"name":"Spreadsheets",  "ext":["xls","xlsx","csv"],              "folder":str(HOME/"Downloads_Sorted"/"Spreadsheets")},
    {"name":"Archives",      "ext":["zip","rar","7z","tar","gz"],     "folder":str(HOME/"Downloads_Sorted"/"Archives")},
    {"name":"Installers",    "ext":["exe","msi"],                     "folder":str(HOME/"Downloads_Sorted"/"Installers")},
]

cfg = {"enabled": True, "sorted_count": 0}
if CFG_FILE.exists():
    try: cfg = json.loads(CFG_FILE.read_text())
    except: pass

def save(): CFG_FILE.write_text(json.dumps(cfg, indent=2))
def log(m):
    with open(LOG_FILE,"a",encoding="utf-8") as f:
        f.write(f"[{datetime.now():%Y-%m-%d %H:%M:%S}] {m}\n")

def match(filename):
    name = filename.lower()
    ext  = Path(filename).suffix.lstrip(".").lower()
    for r in RULES:
        if "pattern" in r and re.search(r["pattern"], name): return r
        if "ext" in r and ext in r["ext"]: return r
    return None

def move_safe(src, dest_folder):
    d = Path(dest_folder)
    d.mkdir(parents=True, exist_ok=True)
    dst = d / Path(src).name
    if dst.exists():
        dst = d / f"{Path(src).stem}_{int(time.time())}{Path(src).suffix}"
    shutil.move(str(src), str(dst))
    return dst

class Handler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory: return
        log(f"Detected: {event.src_path}")
        time.sleep(2)
        if not cfg.get("enabled", True): return
        p = Path(event.src_path)
        if not p.exists():
            log(f"File gone: {p.name}")
            return
        # Skip temp files
        if p.suffix.lower() in [".crdownload", ".tmp", ".part"]:
            return
        r = match(p.name)
        if not r:
            log(f"No rule for: {p.name}")
            return
        try:
            dest = move_safe(p, r["folder"])
            cfg["sorted_count"] += 1
            save()
            log(f"Moved: {p.name} -> {r['name']} ({dest})")
            # Show Windows notification via PowerShell
            notify(p.name, r["name"])
        except Exception as e:
            log(f"ERROR moving {p.name}: {e}")

    def on_modified(self, event):
        if event.is_directory: return
        p = Path(event.src_path)
        # When .crdownload finishes it gets renamed - catch final file
        if p.suffix.lower() in [".crdownload", ".tmp", ".part"]: return

def notify(filename, folder_name):
    try:
        script = f'''
Add-Type -AssemblyName System.Windows.Forms
$notify = New-Object System.Windows.Forms.NotifyIcon
$notify.Icon = [System.Drawing.SystemIcons]::Information
$notify.BalloonTipTitle = "FileSort Pro"
$notify.BalloonTipText = "{filename} moved to {folder_name}"
$notify.Visible = $True
$notify.ShowBalloonTip(4000)
Start-Sleep -Seconds 5
$notify.Dispose()
'''
        import subprocess
        subprocess.Popen(
            ["powershell", "-WindowStyle", "Hidden", "-Command", script],
            creationflags=0x08000000
        )
    except Exception as e:
        log(f"Notify error: {e}")

obs = Observer()
obs.schedule(Handler(), str(DOWNLOADS), recursive=True)
obs.start()
log("FileSort Pro v2 started - watching: " + str(DOWNLOADS))

def make_icon():
    img = Image.new("RGBA",(64,64),(0,0,0,0))
    d   = ImageDraw.Draw(img)
    d.rounded_rectangle([4,4,60,60],radius=14,fill=(108,99,255,255))
    d.rectangle([16,24,48,44],fill=(255,255,255,200))
    d.line([22,32,42,32],fill=(108,99,255,255),width=3)
    d.line([22,38,36,38],fill=(108,99,255,255),width=3)
    return img

import winreg
def add_startup():
    k = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
        r"Software\Microsoft\Windows\CurrentVersion\Run",0,winreg.KEY_SET_VALUE)
    winreg.SetValueEx(k,"FileSortPro",0,winreg.REG_SZ,f'"{sys.executable}" "{__file__}"')
    winreg.CloseKey(k)

def quit_app(icon, _):
    obs.stop()
    try:
        k = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Run",0,winreg.KEY_SET_VALUE)
        winreg.DeleteValue(k,"FileSortPro")
        winreg.CloseKey(k)
    except: pass
    icon.stop()

def toggle(icon, _):
    cfg["enabled"] = not cfg["enabled"]
    save()
    log("Sorting " + ("enabled" if cfg["enabled"] else "paused"))

add_startup()

menu = pystray.Menu(
    item(lambda t: f"Sorted: {cfg.get('sorted_count',0)} files", lambda i,it: None, enabled=False),
    pystray.Menu.SEPARATOR,
    item(lambda t: "Pause sorting" if cfg.get("enabled") else "Resume sorting", toggle),
    item("Open log", lambda i,it: os.startfile(str(LOG_FILE))),
    item("Open Downloads", lambda i,it: os.startfile(str(DOWNLOADS))),
    pystray.Menu.SEPARATOR,
    item("Quit", quit_app),
)
icon = pystray.Icon("FileSortPro", make_icon(), "FileSort Pro - Running", menu)
icon.run()
'@

$trayScript | Out-File -FilePath "$installDir\filesort_tray.py" -Encoding UTF8
Write-Host "Script updated" -ForegroundColor Green

# Relaunch
Write-Host "Relaunching FileSort Pro..." -ForegroundColor Cyan
Start-Process pythonw.exe -ArgumentList "`"$installDir\filesort_tray.py`""
Start-Sleep -Seconds 3

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host " FileSort Pro v2 is now running!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host " Now try downloading any file in Chrome" -ForegroundColor White
Write-Host " Check the log after - it now logs everything" -ForegroundColor White
Write-Host ""
Write-Host "Press any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
