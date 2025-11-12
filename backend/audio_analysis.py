#!/usr/bin/env python3
# === AI-AMV-STUDIO — Termux Audio Analyzer ===
# Uses ffmpeg + pure python for BPM + mood detection

import subprocess
import re
import sys
import json
import os
import math

def ffmpeg_stats(path):
    cmd = f'ffprobe -v quiet -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "{path}"'
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    try:
        duration = float(result.stdout.strip())
    except:
        duration = 0.0

    # volume
    cmd_vol = (
        f'ffmpeg -i "{path}" -af "volumedetect" -f null - 2>&1 | grep mean_volume'
    )
    res = subprocess.run(cmd_vol, shell=True, capture_output=True, text=True)
    try:
        mean_vol = re.findall(r"mean_volume:\s*(-?\d+\.?\d*)", res.stdout)
        mean_vol = float(mean_vol[0]) if mean_vol else -20.0
    except:
        mean_vol = -20.0

    return duration, mean_vol

def extract_wave(path):
    """Extract PCM waveform using ffmpeg — pure python compatible"""
    cmd = f'ffmpeg -i "{path}" -ac 1 -ar 8000 -f s16le - 2>/dev/null'
    raw = subprocess.run(cmd, shell=True, capture_output=True).stdout
    data = []
    for i in range(0, len(raw), 2):
        sample = int.from_bytes(raw[i:i+2], "little", signed=True)
        data.append(sample / 32768.0)
    return data

def estimate_bpm(samples, sr=8000):
    if len(samples) < sr:
        return 110

    # envelope
    energy = [abs(s) for s in samples]

    # peak detect
    peaks = []
    threshold = sum(energy) / len(energy)
    for i in range(1, len(energy)-1):
        if energy[i] > threshold and energy[i] > energy[i-1] and energy[i] > energy[i+1]:
            peaks.append(i)

    if len(peaks) < 2:
        return 120

    intervals = []
    for i in range(1, len(peaks)):
        intervals.append((peaks[i] - peaks[i-1]) / sr)

    if len(intervals) == 0:
        return 125

    avg_interval = sum(intervals) / len(intervals)
    bpm = 60 / avg_interval
    return int(max(60, min(bpm, 200)))

def detect_mood(bpm, volume, energy):
    if bpm > 160:
        return "aggressive"
    if bpm > 130:
        return "energetic"
    if bpm < 85 and volume < -18:
        return "sad"
    if bpm < 100:
        return "calm"
    if 100 <= bpm <= 130:
        return "romantic"
    return "cinematic"

def analyze(path):
    if not os.path.exists(path):
        return {"error": f"{path} not found"}

    duration, volume = ffmpeg_stats(path)
    samples = extract_wave(path)

    if len(samples) == 0:
        return {"error": "decode_failed"}

    energy = sum(abs(s) for s in samples) / len(samples)
    bpm = estimate_bpm(samples)

    mood = detect_mood(bpm, volume, energy)

    return {
        "duration": round(duration, 2),
        "mean_volume": f"{round(volume, 2)} dB",
        "bpm": bpm,
        "energy": round(energy, 4),
        "mood": mood
    }

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: audio_analysis.py <audio file>")
        sys.exit(1)

    path = sys.argv[1]
    print(json.dumps(analyze(path), indent=2))
