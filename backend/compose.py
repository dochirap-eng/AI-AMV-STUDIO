#!/usr/bin/env python3
# === AI-AMV-STUDIO — COMPOSE ENGINE ===
# Builds final AMV timeline from audio analysis + scenes + effects
# Works with Creative Boss AI + Gemini Manager

import os, json, time, random
from pathlib import Path

ROOT = Path(os.path.expanduser("~/AI-AMV-STUDIO"))
STORAGE = ROOT / "storage"
TEMP = STORAGE / "temp"
OUTPUT = STORAGE / "output"

def log(msg):
    print(f"[COMPOSE] {time.strftime('%H:%M:%S')} {msg}", flush=True)

# ---------------------------------------
#  EFFECT PRESETS (Creative Boss AI)
# ---------------------------------------
TRANSITIONS = [
    "fade", "slide_left", "slide_right", "whip", "zoom_in",
    "zoom_out", "flash", "rgb_split", "shake", "film_glow"
]

MOOD_EFFECTS = {
    "aggressive": ["shake", "flash", "rgb_split", "whip"],
    "epic": ["zoom_in", "zoom_out", "whip", "cinematic_glow"],
    "sad": ["fade", "soft_glow", "blur"],
    "romantic": ["fade", "glow", "smooth_pan"],
    "cinematic": ["film_glow", "smooth_pan", "fade"]
}

# ---------------------------------------
# BUILD SINGLE CLIP BLOCK
# ---------------------------------------
def make_block(clip, start, end, effect):
    return {
        "clip": clip,
        "start": start,
        "end": end,
        "duration": round(end - start, 2),
        "effect": effect
    }

# ---------------------------------------
# GENERATE TIMELINE BASED ON AUDIO
# ---------------------------------------
def generate_timeline(task):
    mood = task.get("analysis", {}).get("mood", "cinematic")
    bpm = task.get("analysis", {}).get("bpm", 120)
    sub = task.get("analysis", {}).get("sub_mood", "flow")

    scenes = task.get("scenes", [])
    clips = task.get("scene_clips", [])

    if not scenes or not clips:
        log("⚠ No scenes/clips → fallback timeline.")
        return [make_block(None, 0, 5, "fade")]

    timeline = []
    beat_length = 60 / bpm  # seconds per beat

    log(f"🎵 BPM={bpm}, beat={beat_length:.2f}s, mood={mood}")

    for i, sc in enumerate(scenes):
        s, e = sc["start"], sc["end"]
        dur = e - s
        if dur <= 0:
            continue

        effect_pool = MOOD_EFFECTS.get(mood, TRANSITIONS)
        effect = random.choice(effect_pool)

        clip = clips[i % len(clips)]

        block = make_block(clip, s, e, effect)
        timeline.append(block)

    # Shorten to match beat subdivisions
    for t in timeline:
        beats = max(1, int(t["duration"] / beat_length))
        t["beats"] = beats

    log(f"🎬 Timeline blocks: {len(timeline)}")
    return timeline

# ---------------------------------------
# SAVE TIMELINE JSON
# ---------------------------------------
def save_timeline(task_id, timeline):
    out_path = TEMP / f"{task_id}_timeline.json"
    with open(out_path, "w") as f:
        json.dump(timeline, f, indent=2)
    return out_path

# ---------------------------------------
# MAIN COMPOSE FUNCTION
# ---------------------------------------
def compose_task(task_json_path):
    try:
        task = json.load(open(task_json_path))
    except Exception as e:
        log(f"❌ Cannot read task: {e}")
        return False

    task_id = task.get("id", Path(task_json_path).stem)
    log(f"🧠 Building timeline for {task_id}")

    timeline = generate_timeline(task)
    timeline_path = save_timeline(task_id, timeline)

    task["timeline"] = str(timeline_path)
    with open(task_json_path, "w") as f:
        json.dump(task, f, indent=2)

    log(f"✅ Timeline saved: {timeline_path}")
    return True

# ---------------------------------------
# CLI
# ---------------------------------------
if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: compose.py <task.json>")
        exit(1)
    ok = compose_task(sys.argv[1])
    print("OK" if ok else "FAIL")
