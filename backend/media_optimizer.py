#!/usr/bin/env python3
# ============================================================
#  AI-AMV-STUDIO — Media Optimizer (v3.0)
#  HD Enhance + Compress + Smart Dedup + Crash Protection
# ============================================================

import os
import time
import subprocess
from pathlib import Path

ROOT = Path.home() / "AI-AMV-STUDIO" / "storage"
OUTPUT = ROOT / "output"
TEMP = ROOT / "temp"
LOGS = ROOT / "logs"
LOGS.mkdir(parents=True, exist_ok=True)

LOG_FILE = LOGS / "media_optimizer.log"

def log(msg):
    ts = time.strftime("[%H:%M:%S]")
    line = f"{ts} 🧼 {msg}"
    print(line, flush=True)
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")


# ------------------------------------------------------------
# ✔ SMART COMPRESSOR (CRF auto based on file size)
# ------------------------------------------------------------
def compress_video(path):
    orig_size = os.path.getsize(path)

    # Auto CRF logic
    if orig_size < 10 * 1024 * 1024:  # < 10MB
        crf = 25
    elif orig_size < 50 * 1024 * 1024:  # < 50MB
        crf = 28
    else:
        crf = 30

    out = path.replace(".mp4", "_optimized.mp4")

    cmd = (
        f'ffmpeg -i "{path}" -vcodec libx264 -preset veryfast '
        f"-crf {crf} -b:v 1M -bufsize 1M -threads 4 "
        f'-movflags +faststart "{out}" -y'
    )

    subprocess.call(cmd, shell=True)
    log(f"✨ Optimized: {os.path.basename(out)} ({crf} CRF)")


# ------------------------------------------------------------
# ✔ PROTECT DOUBLE PROCESS
# ------------------------------------------------------------
def already_optimized(filename):
    return filename.endswith("_optimized.mp4") or filename.endswith("_enhanced.mp4")


# ------------------------------------------------------------
# ✔ AI ENHANCER (Future TensorPix integration)
# ------------------------------------------------------------
def enhance_video(path):
    enhanced = path.replace(".mp4", "_enhanced.mp4")

    # Basic FFmpeg sharpen filter (future upgrade: TensorPix API)
    cmd = (
        f'ffmpeg -i "{path}" -vf "unsharp=7:7:1.0:7:7:0.0" '
        f'-c:v libx264 -preset fast "{enhanced}" -y'
    )
    subprocess.call(cmd, shell=True)

    log(f"🔧 Enhanced: {os.path.basename(enhanced)}")


# ------------------------------------------------------------
# ✔ CLEAN TEMP (but protect edit_plan.json)
# ------------------------------------------------------------
def clean_temp():
    for f in TEMP.iterdir():
        if f.name.endswith("_edit_plan.json"):
            continue
        if f.is_file():
            try:
                f.unlink()
            except:
                pass
    log("🗑 Temp cleaned.")


# ------------------------------------------------------------
# ✔ MAIN LOOP
# ------------------------------------------------------------
def optimize_loop():
    log("🚀 Media Optimizer started...")

    while True:
        for f in OUTPUT.iterdir():
            if not f.name.endswith(".mp4"):
                continue
            if already_optimized(f.name):
                continue

            # STEP 1: Enhancement
            enhance_video(str(f))

            # STEP 2: Compression
            compress_video(str(f))

        clean_temp()
        time.sleep(60)  # run every 60 sec


if __name__ == "__main__":
    optimize_loop()
