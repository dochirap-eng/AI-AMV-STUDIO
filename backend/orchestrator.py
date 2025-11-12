import os, time, json, subprocess, random

STORAGE = os.path.expanduser("~/AI-AMV-STUDIO/storage")
TEMP = os.path.join(STORAGE, "temp")
OUTPUT = os.path.join(STORAGE, "output")

def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] 🤖 {msg}", flush=True)

def detect_pending_tasks():
    tasks = [
        os.path.join(TEMP, f) for f in os.listdir(TEMP)
        if f.startswith("task_") and f.endswith(".json") and "_auto_plan" not in f
    ]
    return tasks

def safe_load_task(path):
    try:
        with open(path) as f:
            task = json.load(f)
        if not isinstance(task, dict):
            log(f"⚠️ Invalid task format in {path}, skipping.")
            return None
        if "id" not in task:
            task["id"] = os.path.basename(path).replace(".json", "")
        return task
    except Exception as e:
        log(f"⚠️ Failed to load {path}: {e}")
        return None

def analyze_audio(task):
    log(f"🎵 Analyzing audio for {task['id']} ...")
    bpm = random.randint(80, 160)
    mood = random.choice(["sad", "epic", "romantic", "dark", "motivational"])
    task["analysis"] = {"bpm": bpm, "mood": mood}
    return task

def auto_find_clips(task):
    log(f"🎬 Finding clips for mood: {task['analysis']['mood']}")
    clips = [f"/sample_clips/{task['analysis']['mood']}_{i}.mp4" for i in range(1, 4)]
    task["auto_clips"] = clips
    return task

def generate_edit_plan(task):
    log("🧩 Generating edit plan...")
    plan = [{"clip": c, "start": 0, "end": 5, "effect": "fade"} for c in task["auto_clips"]]
    plan_path = os.path.join(TEMP, f"{task['id']}_auto_plan.json")
    with open(plan_path, "w") as f:
        json.dump(plan, f, indent=2)
    task["plan_path"] = plan_path
    log(f"📋 Edit plan saved: {plan_path}")
    return task

def render_auto_video(task):
    output_name = f"auto_{task['id']}.mp4"
    output_path = os.path.join(OUTPUT, output_name)
    log("🎞️ Rendering auto video...")
    subprocess.call(
        f"ffmpeg -f lavfi -i color=c=black:s=640x360:d=5 -y {output_path}",
        shell=True
    )
    task["output"] = output_path
    log(f"✅ Rendered: {output_path}")
    return task

def run_auto_mode():
    log("🚀 AI Auto Mode started...")
    while True:
        pending = detect_pending_tasks()
        if not pending:
            log("💤 No new tasks... waiting 30s.")
            time.sleep(30)
            continue
        for path in pending:
            if "_auto_plan" in path:
                log(f"⚠️ Skipped non-task file: {os.path.basename(path)}")
                continue
            task = safe_load_task(path)
            if not task:
                continue
            task = analyze_audio(task)
            task = auto_find_clips(task)
            task = generate_edit_plan(task)
            task = render_auto_video(task)
            with open(path, "w") as f:
                json.dump(task, f, indent=2)
            log(f"🎉 Task {task['id']} completed!\n")
        time.sleep(10)

if __name__ == "__main__":
    run_auto_mode()
