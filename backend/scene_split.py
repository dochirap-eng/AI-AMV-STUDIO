#!/usr/bin/env python3
# AI-AMV-STUDIO — Scene Splitter (Creative Boss friendly)
# Simple, fast, Termux-friendly scene detection using ffmpeg scene filter

import os, sys, json, time, subprocess
from pathlib import Path

ROOT = Path(os.path.expanduser("~/AI-AMV-STUDIO"))
STORAGE = ROOT / "storage"
TEMP = STORAGE / "temp"
OUTPUT = STORAGE / "output"

def log(msg):
    print(f"[SCENE] {time.strftime('%H:%M:%S')} {msg}", flush=True)

def ensure_dirs():
    for d in (STORAGE, TEMP, OUTPUT):
        d.mkdir(parents=True, exist_ok=True)

def detect_scenes_ffmpeg(video_path, threshold=0.4):
    """
    Uses ffmpeg scene detection filter to output timestamps.
    Returns list of (start_sec, end_sec) tuples (approx).
    """
    if not os.path.exists(video_path):
        raise FileNotFoundError(video_path)

    cmd = (
        f'ffmpeg -hide_banner -loglevel error -i "{video_path}" '
        f'-vf "select=gt(scene\\,{threshold}),showinfo" -f null - 2>&1'
    )
    proc = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    out = proc.stderr

    times = []
    # parse pts_time from showinfo lines
    for line in out.splitlines():
        if "pts_time" in line:
            # try to extract pts_time=VALUE
            try:
                part = [p for p in line.split() if "pts_time" in p][0]
                t = float(part.split('=')[1])
                times.append(t)
            except:
                continue

    if not times:
        # fallback: split into 5s chunks for short demo
        import math
        duration = get_duration(video_path)
        if duration <= 0:
            return []
        step = 4
        chunks = []
        t = 0.0
        while t < duration:
            chunks.append((t, min(duration, t + step)))
            t += step
        return chunks

    # convert timestamps to intervals (start, end)
    intervals = []
    prev = 0.0
    for t in times:
        intervals.append((prev, t))
        prev = t
    # last chunk
    duration = get_duration(video_path)
    if duration and prev < duration:
        intervals.append((prev, duration))
    return intervals

def get_duration(path):
    try:
        cmd = f'ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "{path}"'
        res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return float(res.stdout.strip())
    except:
        return 0.0

def create_scene_clips(video_path, scenes, out_dir):
    """
    For each scene interval, create a small clip file path (does not render full unless needed).
    Returns list of clip paths (these can be used later by render manager).
    """
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    clips = []
    for idx, (s, e) in enumerate(scenes, start=1):
        duration = max(0.5, e - s)
        out_file = out_dir / f"{Path(video_path).stem}_scene_{idx}.mp4"
        # create short preview clip (very small) — safe for mobile
        cmd = f'ffmpeg -hide_banner -loglevel error -ss {s} -i "{video_path}" -t {duration} -c:v libx264 -preset veryfast -crf 28 -c:a aac -b:a 64k -y "{out_file}"'
        subprocess.call(cmd, shell=True)
        if out_file.exists():
            clips.append(str(out_file))
    return clips

def scene_split_task(task_json_path):
    """
    task_json_path: path to task JSON (contains uploads or video path).
    This function updates task JSON with scenes and preview clips.
    """
    ensure_dirs()
    try:
        with open(task_json_path) as f:
            task = json.load(f)
    except Exception as e:
        log(f"Failed to read task: {e}")
        return False

    video = task.get("video") or task.get("videos") and task.get("videos")[0]
    if not video or not os.path.exists(video):
        log("No video found in task, skipping scene split.")
        return False

    log(f"Detecting scenes for task {task.get('id') or Path(task_json_path).stem}")
    scenes = detect_scenes_ffmpeg(video)
    if not scenes:
        log("No scenes detected, making fallback chunks.")
        scenes = detect_scenes_ffmpeg(video, threshold=0.1)

    # save scenes to task
    task["scenes"] = [{"start": s, "end": e} for s, e in scenes]

    # create preview clips folder
    previews_dir = STORAGE / "previews" / (task.get("id") or Path(task_json_path).stem)
    clips = create_scene_clips(video, scenes[:8], previews_dir)  # limit to first 8 previews
    task["scene_clips"] = clips

    # write back
    with open(task_json_path, "w") as f:
        json.dump(task, f, indent=2)

    log(f"Scene split complete — {len(scenes)} scenes, {len(clips)} previews created.")
    return True

# CLI
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: scene_split.py <task.json>")
        sys.exit(1)
    ok = scene_split_task(sys.argv[1])
    print("OK" if ok else "FAIL")
