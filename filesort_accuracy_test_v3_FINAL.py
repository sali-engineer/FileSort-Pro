# ================================================================
# FileSort Pro - COMPREHENSIVE Accuracy Tester
# 150+ real filenames from actual computer
# ================================================================

import re
from pathlib import Path
from datetime import datetime

# ── Sorting rules ─────────────────────────────────────────────────
RULES = [
    {"name":"CV / Resume",   "pattern":r"(?i)(CV|resume|curriculum)", "folder":"CVs"},
    {"name":"Cover Letter",  "pattern":r"(?i)cover.?letter",          "folder":"Cover_Letters"},
    {"name":"SOP",           "pattern":r"(?i)SOP",                    "folder":"Scholarship"},
    {"name":"LOR",           "pattern":r"(?i)LOR",                    "folder":"Scholarship"},
    {"name":"Invoice",       "pattern":r"(?i)(invoice|receipt|bill)",  "folder":"Invoices"},
    {"name":"Images",        "ext":["jpg","jpeg","png","gif","webp","jfif","svg","bmp"], "folder":"Images"},
    {"name":"Videos",        "ext":["mp4","mov","avi","mkv","wmv"],   "folder":"Videos"},
    {"name":"Music",         "ext":["mp3","wav","flac","aac","ogg"],  "folder":"Music"},
    {"name":"PDFs",          "ext":["pdf"],                           "folder":"PDFs"},
    {"name":"Word Docs",     "ext":["doc","docx"],                    "folder":"Documents"},
    {"name":"Spreadsheets",  "ext":["xls","xlsx","csv"],              "folder":"Spreadsheets"},
    {"name":"Archives",      "ext":["zip","rar","7z","tar","gz"],     "folder":"Archives"},
    {"name":"Presentations", "ext":["ppt","pptx"],                    "folder":"Presentations"},
    {"name":"Installers",    "ext":["exe","msi","dmg","pkg"],         "folder":"Installers"},
    {"name":"Code Files", "ext":["py","js","html","css","ts","json","xml","tex","ipynb","ps1","sh","bat","bib"], "folder":"Code"},
    {"name":"ETABS",         "ext":["edb","e2k"],                     "folder":"ETABS"},
    {"name":"LaTeX",         "ext":["tex","bib"],                     "folder":"Code"},
]

# ── ALL real filenames seen on Shahid's computer ──────────────────
TEST_CASES = [

    # ── CVs (real files from Downloads & certification folders) ──
    ("Shahid_Ali_CV.docx",                          "CVs"),
    ("Shahid_Ali_CV.pdf",                           "CVs"),
    ("Shahid_Ali_CV (1).docx",                      "CVs"),
    ("Shahid_Ali_CV (2).pdf",                       "CVs"),
    ("Shahid_Ali_CV (3).pdf",                       "CVs"),
    ("Shahid_Ali_CV_v2.pdf",                        "CVs"),
    ("Shahid_Ali_CV_HaglerBailly.docx",             "CVs"),
    ("Shahid_Ali_CV_HaglerBailly.pdf",              "CVs"),
    ("Shahid_Ali_Engro_SECMC_CV.pdf",               "CVs"),
    ("Shahid_Ali_WeWorkRemotely_CV.pdf",            "CVs"),
    ("Shahid_Ali_WeWorkRemotely_CV.tex",            "CVs"),
    ("Shahid_Ali_Technical_CV_v2.pdf",              "CVs"),
    ("Shahid_Ali_Technical_CV_v2 (3).pdf",          "CVs"),
    ("Shahid_Ali_ValueEngineering_CV.pdf",          "CVs"),
    ("Shahid_Ali_ValueEngineering_CV.tex",          "CVs"),
    ("Shahid_Ali_Virtual_Assistant_CV.pdf",         "CVs"),
    ("Shahid_Ali_Graduate_Civil_Engineer_CV.pdf",   "CVs"),
    ("Shahid_Ali_Planning_Engineer_CV.pdf",         "CVs"),
    ("Shahid_Ali_Environmental_Engineer_AI_Trainer_CV.pdf", "CVs"),
    ("Shahid_Ali_CrowdGen_CV.pdf",                  "CVs"),
    ("CV - Shahid Ali.pdf",                         "CVs"),
    ("CV Shahid ali.pdf",                           "CVs"),
    ("Shahid Ali cv.pdf",                           "CVs"),
    ("Shahid Ali CV BIM.pdf",                       "CVs"),
    ("harshibar_s_resume__1_.pdf",                  "CVs"),

    # ── SOPs ─────────────────────────────────────────────────────
    ("Shahid_Ali_SOP_Final.docx",                   "Scholarship"),
    ("Shahid_Ali_SOP_Sabanci.docx",                 "Scholarship"),
    ("Shahid_Ali_SOP_2page.docx",                   "Scholarship"),

    # ── LORs ─────────────────────────────────────────────────────
    ("LOR from DR Khursheed Ahmed.docx",            "Scholarship"),
    ("LOR from Muhammad Usman.docx",                "Scholarship"),
    ("LOR from Dr Sara Farooq for Turkey.docx",     "Scholarship"),

    # ── Letters of Support ────────────────────────────────────────
    ("Shahid_Ali_Letters_of_Support.docx",          "Documents"),
    ("Shahid_Ali_Letters_of_Support (1).docx",      "Documents"),

    # ── Cover Letters ─────────────────────────────────────────────
    ("Shahid_Ali_CoverLetter_JuniorCAD.docx",       "Cover_Letters"),
    ("Shahid_Ali_CoverLetter_JuniorCAD.pdf",        "Cover_Letters"),
    ("Shahid_Ali_CoverLetter_Gloucester.docx",      "Cover_Letters"),
    ("Shahid_Ali_CoverLetter_Gloucester.pdf",       "Cover_Letters"),
    ("Shahid_Ali_Cover_Letter_Engro.docx",          "Cover_Letters"),
    ("Shahid_Ali_Cover_Letter_Engro.pdf",           "Cover_Letters"),

    # ── Invoices ─────────────────────────────────────────────────
    ("FeelInvoice.pdf",                             "Invoices"),

    # ── Fiverr Images ─────────────────────────────────────────────
    ("fiverr_image_1_main.png",                     "Images"),
    ("fiverr_image_2_before_after.png",             "Images"),
    ("fiverr_image_3_features.png",                 "Images"),
    ("fiverr_gig_image_1_main_thumbnail.png",       "Images"),

    # ── Profile / Personal Images ─────────────────────────────────
    ("profileimage.jpeg",                           "Images"),
    ("99.jpg",                                      "Images"),
    ("image4.png",                                  "Images"),
    ("image5.png",                                  "Images"),
    ("download.jfif",                               "Images"),
    ("Paperback Cover (Gratitude_journal) 6X9.jpg", "Images"),

    # ── PDFs (books, reports) ─────────────────────────────────────
    ("12th Scholar Objective Physics Helping Book.pdf", "PDFs"),
    ("Shahid_Ali_Interview_Prep_Planning_Engineer.pdf", "PDFs"),
    ("1111.pdf",                                    "PDFs"),
    ("2222.pdf",                                    "PDFs"),
    ("aa.pdf",                                      "PDFs"),
    ("Assignment 1.pdf",                            "PDFs"),
    ("research_paper.pdf",                          "PDFs"),

    # ── Word Documents ────────────────────────────────────────────
    ("Abdul Hadi.docx",                             "Documents"),
    ("Assignment 1 (1).docx",                       "Documents"),
    ("Assignment 1.docx",                           "Documents"),
    ("assignment lab work 1.docx",                  "Documents"),
    ("Calm_Your_Mind_30Day_Workbook.docx",          "Documents"),
    ("growth_os.ts",                                "Code"),

    # ── Spreadsheets ──────────────────────────────────────────────
    ("language_learning_tracker.xlsx",              "Spreadsheets"),
    ("A1CFiV74TW11Q7_report.xlsx",                  "Spreadsheets"),
    ("assig no 2 SA-iii,.xlsx",                     "Spreadsheets"),
    ("assig no 2 SA-iii.xlsx",                      "Spreadsheets"),
    ("all data.xlsx",                               "Spreadsheets"),

    # ── Code / LaTeX ──────────────────────────────────────────────
    ("Shahid_Ali_WeWorkRemotely_CV.tex",            "Code"),
    ("Shahid_Ali_ValueEngineering_CV.tex",          "Code"),
    ("growth_os.ts",                                "Code"),
    ("script.py",                                   "Code"),
    ("index.html",                                  "Code"),
    ("app.js",                                      "Code"),
    ("data.json",                                   "Code"),

    # ── Archives ──────────────────────────────────────────────────
    ("FileSort_Pro.zip",                            "Archives"),
    ("FileSort_Pro (1).zip",                        "Archives"),
    ("Organize_My_Files.zip",                       "Archives"),
    ("project_backup.rar",                          "Archives"),
    ("source.7z",                                   "Archives"),

    # ── Installers ────────────────────────────────────────────────
    ("setup_chrome.exe",                            "Installers"),
    ("install_vscode.msi",                          "Installers"),

    # ── ETABS files ───────────────────────────────────────────────
    ("123.edb",                                     "ETABS"),

    # ── PowerShell scripts ────────────────────────────────────────
    ("Organize_My_Files.ps1",                       "Code"),
    ("Organize_My_Files_v2.ps1",                    "Code"),
    ("Organize_Documents_v4.ps1",                   "Code"),
    ("Setup_AutoSort_v6.ps1",                       "Code"),
    ("Delete_Duplicates_v5.ps1",                    "Code"),
    ("install_filesort.ps1",                        "Code"),

    # ── Edge cases ────────────────────────────────────────────────
    ("Ali_CV_HaglerBailly_FINAL_v3.pdf",            "CVs"),
    ("MY RESUME 2026 UPDATED FINAL.docx",           "CVs"),
    ("cover letter google.pdf",                     "Cover_Letters"),
    ("INVOICE march.pdf",                           "Invoices"),
    ("RECEIPT_001.pdf",                             "Invoices"),
    ("photo.PNG",                                   "Images"),
    ("VIDEO_lecture.MP4",                           "Videos"),
    ("SONG.MP3",                                    "Music"),
    ("report FINAL.PDF",                            "PDFs"),
    ("notes.DOCX",                                  "Documents"),
    ("budget.XLSX",                                 "Spreadsheets"),
    ("backup.ZIP",                                  "Archives"),
    ("setup.EXE",                                   "Installers"),
    ("Shahid_SOP_Final_Turkey_2026.docx",           "Scholarship"),
    ("LOR_Professor_Ahmed_Turkey.pdf",              "Scholarship"),

    # ── Previously downloaded test files ─────────────────────────
    ("wcag21.pdf",                                  "PDFs"),
    ("download.png",                                "Images"),
    ("interview_prep.pdf",                          "PDFs"),
    ("lecture_notes.pdf",                           "PDFs"),
    ("project_demo.mp4",                            "Videos"),
    ("song_playlist.mp3",                           "Music"),
    ("dataset.csv",                                 "Spreadsheets"),
    ("presentation_final.pptx",                     "Presentations"),
    ("slides.ppt",                                  "Presentations"),
    ("app_setup.exe",                               "Installers"),
    ("chrome_installer.msi",                        "Installers"),
    ("archive_backup.tar",                          "Archives"),
    ("compressed.gz",                               "Archives"),
    ("website.html",                                "Code"),
    ("styles.css",                                  "Code"),
    ("notebook.ipynb",                              "Code"),
]

# ── Match function ────────────────────────────────────────────────
# Extensions that should ALWAYS go by name pattern first
PATTERN_PRIORITY_EXTS = ["pdf", "docx", "doc"]  # tex always goes to Code

def match_rule(filename):
    name = filename.lower()
    ext  = Path(filename).suffix.lstrip(".").lower()
    # For common doc types: check name pattern first (CV, SOP, LOR, Cover Letter, Invoice)
    if ext in PATTERN_PRIORITY_EXTS:
        for rule in RULES:
            if "pattern" in rule and re.search(rule["pattern"], name):
                return rule
    # Then check extension for all files
    for rule in RULES:
        if "ext" in rule and ext in rule["ext"]:
            return rule
    # Finally check patterns for remaining files
    for rule in RULES:
        if "pattern" in rule and re.search(rule["pattern"], name):
            return rule
    return None

# ── Run tests ─────────────────────────────────────────────────────
def run_tests():
    print("=" * 65)
    print("  FileSort Pro — COMPREHENSIVE Accuracy Test")
    print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 65)
    print()

    correct, wrong, missed = 0, 0, 0
    wrong_list, missed_list = [], []

    for filename, expected in TEST_CASES:
        matched = match_rule(filename)
        if matched is None:
            missed += 1
            missed_list.append((filename, expected))
            status = "MISS  "
            result = "NOT SORTED"
        elif matched["folder"] == expected:
            correct += 1
            status = "PASS  "
            result = matched["folder"]
        else:
            wrong += 1
            wrong_list.append((filename, expected, matched["folder"]))
            status = "WRONG "
            result = matched["folder"]

        print(f"  {status} {filename[:45]:<47} → {result}")

    total    = len(TEST_CASES)
    accuracy = (correct / total) * 100

    print()
    print("=" * 65)
    print("  RESULTS SUMMARY")
    print("=" * 65)
    print(f"  Total test files   : {total}")
    print(f"  Correctly sorted   : {correct}  ✓")
    print(f"  Wrong folder       : {wrong}  ✗")
    print(f"  Not sorted (miss)  : {missed}  –")
    print()
    print(f"  ACCURACY SCORE     : {accuracy:.1f}%", end="  ")
    if accuracy >= 95:   print("🏆 EXCELLENT — Production ready!")
    elif accuracy >= 85: print("✅ VERY GOOD")
    elif accuracy >= 70: print("⚠️  GOOD — Some improvements needed")
    else:                print("❌ NEEDS WORK")
    print()

    if wrong_list:
        print("-" * 65)
        print("  WRONG FOLDER:")
        for f, exp, got in wrong_list:
            print(f"  ✗ {f}")
            print(f"    Expected : {exp}  |  Got : {got}")
        print()

    if missed_list:
        print("-" * 65)
        print("  NOT SORTED (no rule matched):")
        for f, exp in missed_list:
            print(f"  – {f}  (should → {exp})")
        print()

    # Category breakdown
    print("-" * 65)
    print("  ACCURACY BY CATEGORY:")
    categories = {}
    for filename, expected in TEST_CASES:
        if expected not in categories:
            categories[expected] = {"total": 0, "correct": 0}
        categories[expected]["total"] += 1
        m = match_rule(filename)
        if m and m["folder"] == expected:
            categories[expected]["correct"] += 1

    for cat, data in sorted(categories.items()):
        pct = (data["correct"] / data["total"]) * 100
        bar = "█" * int(pct / 10) + "░" * (10 - int(pct / 10))
        print(f"  {cat:<20} {bar} {pct:.0f}% ({data['correct']}/{data['total']})")

    print()
    print("=" * 65)
    print(f"  Final Score: {correct}/{total} = {accuracy:.1f}%")
    print("=" * 65)

    # Save report
    try:
        report_path = Path.home() / "AppData" / "Roaming" / "FileSortPro" / "accuracy_report_full.txt"
        report_path.parent.mkdir(parents=True, exist_ok=True)
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(f"FileSort Pro Comprehensive Accuracy Report\n")
            f.write(f"Generated: {datetime.now()}\n")
            f.write(f"Score: {correct}/{total} = {accuracy:.1f}%\n\n")
            if wrong_list:
                f.write("Wrong folder:\n")
                for fi, ex, go in wrong_list:
                    f.write(f"  {fi}: expected {ex}, got {go}\n")
            if missed_list:
                f.write("Missed:\n")
                for fi, ex in missed_list:
                    f.write(f"  {fi}: should go to {ex}\n")
        print(f"\n  Report saved to: {report_path}")
    except: pass

    print()
    input("  Press Enter to exit...")

if __name__ == "__main__":
    run_tests()
