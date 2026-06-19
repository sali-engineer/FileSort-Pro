# FileSort Pro 🗂️
**AI-powered file organization system Chrome Extension + Python Windows App**

![Python](https://img.shields.io/badge/Python-3.x-blue) ![JavaScript](https://img.shields.io/badge/JavaScript-ES6-yellow) ![Accuracy](https://img.shields.io/badge/Accuracy-98.3%25-brightgreen) ![License](https://img.shields.io/badge/License-MIT-green)

---

## The Problem
Every computer user faces the same problem: files downloaded from the internet end up scattered randomly. CVs mixed with images, PDFs mixed with installers, important documents buried under random screenshots. Users waste hours manually organizing their Downloads folder only for it to become messy again within days.

## The Solution
FileSort Pro is a two-part automation system that works silently in the background and organizes every file the moment it is downloaded **without any user input.**

| Metric | Result |
|--------|--------|
| Files sorted in testing | 800+ |
| Sorting rules built-in | 13 |
| Setup time | 2 minutes |
| Accuracy (120 file test) | **98.3%** |
| Manual work after install | **Zero** |

---

## How It Works

### Part 1 — Chrome Browser Extension
- Monitors every file downloaded through Chrome or Edge in real time
- Matches filename and extension against 13 built-in sorting rules
- Shows an instant desktop notification with the suggested folder
- Dashboard popup shows activity history and lets user toggle rules on/off

### Part 2 — Windows Background App (System Tray)
- Runs silently in the background, starts automatically on every Windows login
- Watches the Downloads folder using a real-time file system watcher
- Physically moves files to the correct organized folder automatically
- Logs every action with timestamps full audit trail
- System tray icon with pause/resume, open log, open Downloads options

---

## Accuracy Results

Tested on **120 real files** across 15 categories:

| Category | Accuracy |
|----------|----------|
| Archives | 100% (8/8) |
| CVs | 93% (25/27) |
| Code | 100% (17/17) |
| Cover Letters | 100% (7/7) |
| Documents | 100% (8/8) |
| ETABS Files | 100% (1/1) |
| Images | 100% (12/12) |
| Installers | 100% (5/5) |
| Invoices | 100% (3/3) |
| Music | 100% (2/2) |
| PDFs | 100% (11/11) |
| Presentations | 100% (2/2) |
| Scholarship | 100% (8/8) |
| Spreadsheets | 100% (7/7) |
| Videos | 100% (2/2) |

**Final Score: 118/120 = 98.3% — Production Ready ✅**

---

## Technology Stack

| Component | Technology |
|-----------|-----------|
| Browser Extension | JavaScript, Chrome APIs, Service Worker |
| System Tray App | Python 3, Pystray, Pillow |
| File Watcher | Watchdog library |
| Notifications | PowerShell Windows Toast |
| File Matching | Regex pattern matching |
| Installer | PowerShell script |

---

## Installation

### Chrome Extension
1. Open Chrome → go to `chrome://extensions/`
2. Enable **Developer Mode** (top right)
3. Click **Load unpacked**
4. Select the `FileSort_Pro` folder

### Windows Tray App
1. Make sure Python 3 is installed
2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Run the PowerShell installer:
```powershell
.\install_filesort_v2.ps1
```
4. The app starts automatically on Windows login

---

## Future Roadmap
- Train a lightweight ML classifier (Random Forest / BERT) on filename patterns
- NLP-based content analysis read PDF/DOCX content to determine category
- Personalization engine learns each user's folder preferences over time
- Anomaly detection flags suspicious files
- Cross-platform support macOS and Linux
- Cloud sync auto-upload sorted files to Google Drive / OneDrive

---

## Author
**Shahid Ali**
Civil Engineer & Python Developer | NUST Islamabad 2026
GitHub: [sali-engineer](https://github.com/sali-engineer)

---

*Built and tested June 2026 | Open to collaboration and feedback*
