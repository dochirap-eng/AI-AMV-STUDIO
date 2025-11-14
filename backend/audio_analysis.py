#!/usr/bin/env python3
# === AI-AMV-STUDIO — SUPER INTELLIGENT AUDIO ANALYSIS ENGINE ===
# Creative Boss AI + Deep Mood Logic + Fast FFmpeg Engine

import subprocess
import re
import sys
import json
import os
import math
from statistics import mean

# -----------------------------
# 🔥 FAST LOG
# -----------------------------
def log(x):
    print(f"[AUDIO] {x}", flush=True)

# -----------------------------
# 🎧 BASIC FFPROBE INFO
# -----------------------------
def ffmpeg_stats(path):
    try:
        cmd = f'ffprobe -v quiet -show_entries format=duration -of default=nokey=1:noprint_wrappers=1 "{path}"'
        d = float(subprocess.run(cmd, shell=True, capture_output=True, text=True).stdout.strip())
    except:
        d = 0.0

    # volume detection
    cmd2 = f'ffmpeg -i "{path}" -af "volumedetect" -f null - 2>&1'
    res = subprocess.run(cmd2, shell=True, capture_output=True, text=True)
    vol = re.search(r"mean_volume:\s*(-?\d+\.?\d*)", res.stdout)
    vol = float(vol.group(1)) if vol else -20.0

    return d, vol

# -----------------------------
# 🎼 WAVEFORM + ENERGY
# -----------------------------
def extract_wave(path):
    cmd = f'ffmpeg -i "{path}" -ac 1 -ar 11025 -f s16le - 2>/dev/null'
    raw = subprocess.run(cmd, shell=True, capture_output=True).stdout
    data = []

    for i in range(0, len(raw), 2):
        smp = int.from_bytes(raw[i:i+2], "little", signed=True)
        data.append(smp / 32768.0)

    return data

# -----------------------------
# 🥁 BPM ESTIMATE (Improved)
# -----------------------------
def estimate_bpm(samples, sr=11025):
    if len(samples) < sr:
        return 118

    energy = [abs(x) for x in samples]
    threshold = mean(energy) * 1.2

    peaks = [
        i for i in range(1, len(energy)-1)
        if energy[i] > threshold and energy[i] > energy[i-1] and energy[i] > energy[i+1]
    ]

    if len(peaks) < 3:
        return 120

    intervals = [(peaks[i] - peaks[i-1]) / sr for i in range(1, len(peaks))]
    avg = mean(intervals)
    bpm = int(max(60, min(200, 60 / avg)))
    return bpm

# -----------------------------
# 🎭 ADVANCED MOOD ENGINE
# -----------------------------
def detect_mood(bpm, volume, energy):
    intense = bpm > 145 or energy > 0.12
    soft = bpm < 95 and volume < -17

    if intense:
        return "aggressive"
    if bpm > 130:
        return "epic"
    if soft:
        return "sad"
    if 100 <= bpm <= 125:
        return "romantic"
    return "cinematic"

# -----------------------------
# 🔥 SUB-MOOD (Extra Layer)
# -----------------------------
def detect_submood(bpm, energy):
    if bpm > 160: return "impact"
    if bpm < 85: return "emotional"
    if energy > 0.10: return "hype"
    return "flow"

# -----------------------------
# 🎬 STYLE CLASSIFIER (AMV)
# -----------------------------
def detect_edit_style(bpm, mood):
    if mood == "aggressive": return "velocity"
    if mood == "epic": return "impact"
    if mood == "sad": return "emotional-sync"
    if mood == "romantic": return "smooth-flow"
    return "cinematic-glow"

# -----------------------------
# 🧠 SMART ANALYZE
# -----------------------------
def analyze(path):
    if not os.path.exists(path):
        return {"error": "File not found"}

    duration, volume = ffmpeg_stats(path)
    wave = extract_wave(path)
    if len(wave) == 0:
        return {"error": "Decode error"}

    # energy, bpm
    energy = mean([abs(s) for s in wave])
    bpm = estimate_bpm(wave)

    # main mood
    mood = detect_mood(bpm, volume, energy)
    submood = detect_submood(bpm, energy)
    style = detect_edit_style(bpm, mood)

    return {
        "duration": round(duration, 2),
        "volume": round(volume, 2),
        "bpm": bpm,
        "energy": round(energy, 4),
        "mood": mood,
        "sub_mood": submood,
        "edit_style": style
    }

# -----------------------------
# 🔌 CLI DIRECT CALL
# -----------------------------
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: audio_analysis.py <audiofile>")
        sys.exit(1)

    out = analyze(sys.argv[1])
    print(json.dumps(out, indent=2))
