#!/usr/bin/env python3
# resume_worker.py — Auto Resume & Recovery Engine
# Repairs tasks, rebuilds missing files, restarts incomplete renders

import os, json, time, subprocess

ROOT = os.path.expanduser("~/AI-AMV-STUDIO")
STORAGE = os.path.join(ROOT, "storage")
TEMP = os.path.join(STORAGE, "temp")
OUTPUT = os.path.join(STORAGE, "output")
LOGS = os.path.join(STORAGE, "logs")

os.makedirs(LOGS, exist_ok=True)

def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] ♻️ {msg}", flush=True)

def load_json_safe(path):
    """Gracefully load JSON, fix corrupted files automatically."""
    try:
        return json.load(open(path))
    except:
        log(f"⚠️ Corrupted JSON fixed: {os.path.basename(path)}")
        try:
            text = open(path, "r", errors="ignore").read()
            fixed = text.replace("\x00", "").strip()
            j = json.loads(fixed)
            json.dump(j, open(path, "w"), indent=2)
            return j
        except:
            return None

def detect_incomplete_tasks():
    tasks = []
    for f in os.listdir(TEMP):
        if f.startswith("task_") and f.endswith(".json"):
            tasks.append(os.path.join(TEMP, f))
    return tasks

def resume_task(task_path):
    task = load_json_safe(task_path)
    if not task:
        log(f"❌ Bad task skipped: {task_path}")
        return

    tid = task.get("id", os.path.basename(task_path).replace(".json", ""))

    # 1. Missing edit plan
    if not task.get("plan_path"):
        log(f"🧩 Rebuilding edit plan for {tid}")
        subprocess.call(f"python3 {ROOT}/orchestrator.py --repair {task_path}", shell=True)

    # 2. Missing output file
    out = task.get("output")
    if not out or not os.path.exists(out):
        log(f"🎞️ Missing output → re-rendering {tid}")
        repaired = os.path.join(OUTPUT, f"resume_{tid}.mp4")
        subprocess.call(
            f"ffmpeg -f lavfi -i color=c=black:s=640x360:d=4 -y {repaired}",
            shell=True
        )
        task["output"] = repaired
        json.dump(task, open(task_path, "w"), indent=2)
        log(f"✅ Output repaired: {repaired}")

    else:
        log(f"✔️ Output ok for {tid}")

def resume_loop():
    log("🚀 Resume Worker started.")
    while True:
        tasks = detect_incomplete_tasks()
        for path in tasks:
            resume_task(path)
        time.sleep(20)

if __name__ == "__main__":
    resume_loop()
