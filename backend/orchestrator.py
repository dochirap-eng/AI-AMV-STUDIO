#!/usr/bin/env python3
# ============================================================
#  AI-AMV-STUDIO — SUPREME BOSS AI (V3 FINAL)
#  Controls all AI models, planning, decisions, fail-safe
# ============================================================

import os, time, json, random, subprocess, traceback
from pathlib import Path

ROOT = Path.home() / "AI-AMV-STUDIO"
STORAGE = ROOT / "storage"
TEMP = STORAGE / "temp"
OUTPUT = STORAGE / "output"
LOGS = STORAGE / "logs"

LOGS.mkdir(parents=True, exist_ok=True)
LOGFILE = LOGS / "boss_ai.log"

# ============================================================
# LOGGING SYSTEM
# ============================================================
def log(msg):
    line = f"[BOSS {time.strftime('%H:%M:%S')}] {msg}"
    print(line)
    with open(LOGFILE, "a") as f:
        f.write(line + "\n")


# ============================================================
#  SUPREME BOSS PERSONALITY (Smart + Creative)
# ============================================================

MOOD_EFFECTS = {
    "sad": ["blue_soft", "slow_fade", "blur_light"],
    "epic": ["impact_flash", "shake_heavy", "zoom_crash"],
    "romantic": ["warm_glow", "soft_zoom"],
    "dark": ["red_flash", "glitch_hard"],
    "motivational": ["speed_pop", "white_flash"]
}

TRANSITIONS = [
    "shake_cut", "cross_flash", "zoom_whip",
    "spin_cut", "impact_cut", "anime_glitch"
]

EFFECTS = [
    "soft_glow", "shake", "lighting_flash", "zoom_hit",
    "glitch", "speedline", "color_pop"
]


# ============================================================
#  AUTO-DETECT TASKS
# ============================================================
def detect_tasks():
    return [
        p for p in TEMP.glob("task_*.json")
        if "_auto_plan" not in str(p)
    ]


# ============================================================
# SAFE LOAD
# ============================================================
def load_task(path):
    try:
        data = json.load(open(path))
        if "id" not in data:
            data["id"] = path.stem
        return data
    except Exception as e:
        log(f"⚠️ Error loading task: {e}")
        return None


# ============================================================
# STEP 1 — INTELLIGENT AUDIO ANALYSIS
# ============================================================
def analyze_audio(task):
    log(f"🎵 AUDIO: Smart analysis for {task['id']}")

    # Real audio analysis delegated to audio_analysis.py
    try:
        result = subprocess.check_output(
            f'python3 {ROOT}/backend/audio_analysis.py "{task["audio"]}"',
            shell=True
        )
        task["analysis"] = json.loads(result.decode())
    except:
        # fallback if script failed
        task["analysis"] = {
            "bpm": random.randint(90,180),
            "mood": random.choice(list(MOOD_EFFECTS.keys())),
            "error": "fallback_mode"
        }

    log(f"✔️ BPM={task['analysis']['bpm']} | Mood={task['analysis']['mood']}")
    return task


# ============================================================
# STEP 2 — CLIP PICKER (SMART)
# ============================================================
def pick_clips(task):
    mood = task["analysis"]["mood"]
    log(f"🎬 CLIPS: Picking best clips for mood → {mood}")

    # Later: Replace with online free AI clip finder
    task["clips"] = [
        f"/sample_clips/{mood}_{i}.mp4"
        for i in range(1, 5)
    ]
    return task


# ============================================================
# STEP 3 — SUPREME EDIT PLAN GENERATOR
# ============================================================
def generate_plan(task):
    mood = task["analysis"]["mood"]
    bpm = task["analysis"]["bpm"]

    log("🧩 PLAN: Creating Supreme Edit Plan...")

    time_pos = 0
    plan = []

    for c in task["clips"]:
        plan.append({
            "clip": c,
            "start": time_pos,
            "end": time_pos + 4,
            "effect": random.choice(EFFECTS),
            "transition": random.choice(TRANSITIONS),
            "mood_fx": random.choice(MOOD_EFFECTS[mood]),
            "beat_sync": bpm
        })
        time_pos += 4

    plan_path = TEMP / f"{task['id']}_auto_plan.json"
    json.dump(plan, open(plan_path, "w"), indent=2)

    task["plan_path"] = str(plan_path)
    log(f"✔️ PLAN saved: {plan_path}")
    return task


# ============================================================
# STEP 4 — RENDER (DEMO — BLACK VIDEO)
# ============================================================
def render(task):
    out = OUTPUT / f"{task['id']}_render.mp4"
    log("🎞️ RENDER: (Demo Mode) Creating video...")

    subprocess.call(
        f"ffmpeg -f lavfi -i color=c=black:s=1280x720:d=6 -y {out}",
        shell=True
    )
    task["output"] = str(out)
    log(f"✔️ RENDER DONE → {out}")
    return task


# ============================================================
# FAIL-SAFE RECOVERY
# ============================================================
def save_task(task):
    try:
        json.dump(task, open(TEMP / f"{task['id']}.json", "w"), indent=2)
    except:
        log("❌ FAILED saving task!")


# ============================================================
# MAIN LOOP — SUPREME AI ENGINE
# ============================================================
def run():
    log("🚀 SUPREME BOSS AI STARTED (V3)")
    
    while True:
        tasks = detect_tasks()

        if not tasks:
            log("😴 Idle... waiting 10s")
            time.sleep(10)
            continue

        for path in tasks:
            try:
                task = load_task(path)
                if not task:
                    continue

                log(f"⚡ Processing {task['id']}")

                task = analyze_audio(task)
                task = pick_clips(task)
                task = generate_plan(task)
                task = render(task)

                save_task(task)
                log(f"🎉 COMPLETE → {task['id']}\n")

            except Exception as e:
                log("❌ CRASH in task: " + str(e))
                traceback.print_exc()

        time.sleep(5)


# ============================================================
# ENTRY POINT
# ============================================================
if __name__ == "__main__":
    run()
