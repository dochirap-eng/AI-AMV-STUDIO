#!/usr/bin/env python3
# cloud_sync_manager.py — automatic cloud sync + cleanup

import os, time, shutil, subprocess

ROOT = os.path.expanduser("~/AI-AMV-STUDIO")
STORAGE = os.path.join(ROOT, "storage")
OUTPUT = os.path.join(STORAGE, "output")
BACKUP = os.path.join(ROOT, "cloud_backup")

os.makedirs(BACKUP, exist_ok=True)

def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] ☁️ {msg}", flush=True)

def sync_files():
    files = [f for f in os.listdir(OUTPUT) if f.endswith(".mp4")]
    if not files:
        log("No new output files found.")
        return

    for f in files:
        src = os.path.join(OUTPUT, f)
        dst = os.path.join(BACKUP, f)
        try:
            shutil.copy2(src, dst)
            log(f"✅ Synced {f} → cloud_backup/")
        except Exception as e:
            log(f"❌ Failed to sync {f}: {e}")

def auto_cleanup():
    files = [f for f in os.listdir(OUTPUT) if f.endswith(".mp4")]
    if len(files) > 20:  # keep only 20 latest renders
        files.sort(key=lambda x: os.path.getmtime(os.path.join(OUTPUT, x)))
        for f in files[:-20]:
            try:
                os.remove(os.path.join(OUTPUT, f))
                log(f"🧹 Deleted old output: {f}")
            except:
                pass

def periodic_sync():
    log("🚀 Cloud Sync Manager started.")
    while True:
        sync_files()
        auto_cleanup()
        time.sleep(60 * 10)  # every 10 minutes

if __name__ == "__main__":
    periodic_sync()
