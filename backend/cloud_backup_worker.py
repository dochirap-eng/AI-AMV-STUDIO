#!/usr/bin/env python3
# ==========================================================
#  AI-AMV-STUDIO — Smart Cloud Backup Engine (v1.0)
#  Auto-Backup → Auto-Verify → Auto-Log
#  Works in Termux + Cloud Server + Future WebDAV/S3
# ==========================================================

import os, time, shutil, json
from pathlib import Path

ROOT = Path.home() / "AI-AMV-STUDIO"
STORAGE = ROOT / "storage"
OUTPUT = STORAGE / "output"
BACKUP = ROOT / "cloud_backup"
LOGS = STORAGE / "logs"

BACKUP.mkdir(parents=True, exist_ok=True)
LOGS.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOGS / "backup_engine.log"

# ---------------------------
# LOGGING
# ---------------------------
def log(msg):
    ts = time.strftime("[%Y-%m-%d %H:%M:%S]")
    line = f"{ts} ☁️ {msg}"
    print(line, flush=True)
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")


# ---------------------------
# BACKUP FUNCTION
# ---------------------------
def backup_new_videos():
    files = sorted([f for f in OUTPUT.iterdir() if f.suffix in [".mp4",".mov",".mkv"]])
    if not files:
        log("No video files found to backup.")
        return

    for f in files:
        dst = BACKUP / f.name

        # Already backed up?
        if dst.exists() and dst.stat().st_size == f.stat().st_size:
            log(f"⏩ Already backed up: {f.name}")
            continue

        try:
            shutil.copy2(f, dst)
            log(f"✅ Backed up: {f.name}")
        except Exception as e:
            log(f"❌ Backup failed for {f.name}: {e}")


# ---------------------------
# VERIFY BACKUP
# ---------------------------
def verify_backup():
    vids = [f for f in OUTPUT.iterdir() if f.suffix in [".mp4",".mov",".mkv"]]
    if not vids:
        return

    for f in vids:
        b = BACKUP / f.name
        if not b.exists():
            log(f"⚠️ Missing backup file: {f.name}")
            continue
        if b.stat().st_size < f.stat().st_size * 0.95:
            log(f"❌ Corrupted backup detected: {f.name}")
        else:
            log(f"🟢 Verified backup OK: {f.name}")


# ---------------------------
# AUTO CLEANUP OLD BACKUPS
# ---------------------------
def cleanup_old_backups(limit=50):
    files = sorted(BACKUP.iterdir(), key=lambda x: x.stat().st_mtime)
    if len(files) <= limit:
        return

    to_delete = files[:-limit]
    for f in to_delete:
        try:
            f.unlink()
            log(f"🧹 Deleted old backup: {f.name}")
        except:
            pass


# ---------------------------
# MAIN LOOP
# ---------------------------
def run_loop():
    log("🚀 Cloud Backup Engine started.")
    while True:
        backup_new_videos()
        verify_backup()
        cleanup_old_backups(limit=50)
        time.sleep(300)  # run every 5 minutes


if __name__ == "__main__":
    run_loop()
