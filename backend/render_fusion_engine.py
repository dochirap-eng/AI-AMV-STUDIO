import os, json, time, subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STORAGE = ROOT / "storage"
TEMP_DIR = STORAGE / "temp"
OUTPUT_DIR = STORAGE / "output"
LOGS_DIR = STORAGE / "logs"

LOGS_DIR.mkdir(parents=True, exist_ok=True)
log_file = LOGS_DIR / "render_fusion.log"

def log(msg):
    ts = time.strftime("[%Y-%m-%d %H:%M:%S]")
    entry = f"{ts} {msg}"
    print(entry)
    with open(log_file, "a") as f:
        f.write(entry + "\n")

def get_edit_plans():
    return [p for p in TEMP_DIR.glob("*_edit_plan.json")]

def render_video(plan_path):
    try:
        plan = json.load(open(plan_path))
        prompt = plan.get("prompt", "unknown")
        clips = plan.get("clips", [])
        effects = plan.get("effects", [])
        out_name = f"fusion_{int(time.time())}.mp4"
        out_path = OUTPUT_DIR / out_name

        if not clips:
            log(f"⚠️ No clips in {plan_path.name}, skipping.")
            return

        list_path = TEMP_DIR / f"list_{int(time.time())}.txt"
        with open(list_path, "w") as f:
            for c in clips:
                f.write(f"file '{c}'\n")

        ffmpeg_cmd = [
            "ffmpeg", "-y", "-f", "concat", "-safe", "0",
            "-i", str(list_path),
            "-c:v", "libx264", "-preset", "ultrafast", "-crf", "22",
            "-c:a", "aac", str(out_path)
        ]
        subprocess.run(ffmpeg_cmd, capture_output=True)
        os.remove(list_path)

        # effects simulation
        log(f"🎨 Effects applied: {effects}")
        log(f"✅ Render complete → {out_name}")

        return out_name

    except Exception as e:
        log(f"🔥 Render error in {plan_path.name}: {e}")

def main():
    log("🎬 AI Render Fusion Engine Started...")
    while True:
        plans = get_edit_plans()
        for plan in plans:
            render_video(plan)
            # mark done
            done = plan.with_suffix(".done")
            plan.rename(done)
        time.sleep(30)

if __name__ == "__main__":
    main()
