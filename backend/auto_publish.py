#!/usr/bin/env python3
# ============================================================
# AI-AMV-STUDIO — Ultra Upload Queue Engine (v3.0)
# Handles: upload queue, metadata, priority, dedupe
# Future: YouTube/TeraBox/Mega/Cloudflare direct upload
# ============================================================

import os, time, json, shutil
from pathlib import Path

ROOT = Path.home() / "AI-AMV-STUDIO" / "storage"
OUTPUT = ROOT / "output"
QUEUE = ROOT / "upload_queue"
META = ROOT / "metadata"
LOGS = ROOT / "logs"

QUEUE.mkdir(parents=True, exist_ok=True)
META.mkdir(parents=True, exist_ok=True)
LOGS.mkdir(parents=True, exist_ok=True)

LOG_FILE = LOGS / "auto_publish.log"

# ------------------------------------------------------------
# LOG FUNCTION
# ------------------------------------------------------------
def log(msg):
    ts = time.strftime("[%H:%M:%S]")
    line = f"{ts} 🚀 {msg}"
    print(line, flush=True)
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")


# ------------------------------------------------------------
# CREATE METADATA FILE
# ------------------------------------------------------------
def create_metadata(video_name):
    meta = {
        "file": video_name,
        "created_at": int(time.time()),
        "priority": 1,   # 1 = normal, 2 = high (future)
        "upload_status": "pending",
        "tags": [],
        "platform": "none",  # youtube / meganz / terabox / r2
    }

    meta_path = META / f"{video_name}.json"
    with open(meta_path, "w") as f:
        json.dump(meta, f, indent=2)

    log(f"📝 Metadata created: {video_name}.json")


# ------------------------------------------------------------
# QUEUE MANAGER
# ------------------------------------------------------------
def move_to_queue():
    files = sorted([f for f in OUTPUT.iterdir() if f.suffix == ".mp4"])

    for f in files:
        queue_path = QUEUE / f.name

        # check if already queued
        if queue_path.exists():
            continue

        # copy video to upload_queue
        shutil.copy2(f, queue_path)
        log(f"📤 Added to upload queue: {f.name}")

        # create metadata
        create_metadata(f.name)


# ------------------------------------------------------------
# TRIM QUEUE (avoid huge queue)
# ------------------------------------------------------------
def trim_queue(max_files=30):
    files = sorted(QUEUE.iterdir(), key=lambda x: x.stat().st_mtime)

    while len(files) > max_files:
        old = files.pop(0)
        try:
            old.unlink()
            log(f"🗑 Removed old queue file: {old.name}")
        except:
            pass


# ------------------------------------------------------------
# MAIN LOOP
# ------------------------------------------------------------
def run_auto_publish():
    log("⚡ Auto-Publish Engine Started...")

    while True:
        move_to_queue()
        trim_queue(max_files=30)
        time.sleep(15)   # check every 15 seconds


if __name__ == "__main__":
    run_auto_publish()
