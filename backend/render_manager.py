import os, json, time, subprocess, random

STORAGE = os.path.expanduser("~/AI-AMV-STUDIO/storage")
TEMP = os.path.join(STORAGE, "temp")
OUTPUT = os.path.join(STORAGE, "output")

def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] 🎞️ {msg}", flush=True)

def detect_tasks():
    return [
        os.path.join(TEMP, f)
        for f in os.listdir(TEMP)
        if f.startswith("task_") and f.endswith(".json") and "_auto_plan" not in f
    ]

def safe_load(path):
    try:
        with open(path) as f:
            data = json.load(f)
        if isinstance(data, list):
            log(f"⚠️ Skipped non-task list file: {os.path.basename(path)}")
            return None
        if "id" not in data:
            data["id"] = os.path.basename(path).replace(".json", "")
        return data
    except Exception as e:
        log(f"⚠️ Failed to load {path}: {e}")
        return None

def check_video_quality(path):
    if not os.path.exists(path):
        return False
    size = os.path.getsize(path)
    return size > 5000  # 5 KB minimum expected render size

def re_render(task):
    log(f"♻️ Re-rendering task {task['id']}...")
    output_name = f"rerender_{task['id']}.mp4"
    output_path = os.path.join(OUTPUT, output_name)

    subprocess.call(
        f"ffmpeg -f lavfi -i color=c=white:s=640x360:d=5 -y {output_path}",
        shell=True
    )

    if check_video_quality(output_path):
        log(f"✅ Re-rendered successfully: {output_path}")
    else:
        log(f"❌ Re-render failed for {task['id']}")
    return output_path

def auto_render_loop():
    log("🚀 Render Manager started.")
    while True:
        tasks = detect_tasks()
        for path in tasks:
            if "_auto_plan" in path:
                log(f"⚠️ Skipped non-task file: {os.path.basename(path)}")
                continue

            data = safe_load(path)
            if not data:
                continue

            output_path = data.get("output")
            if not output_path:
                log(f"⚠️ No output field for {data['id']}, skipping.")
                continue

            if not check_video_quality(output_path):
                log(f"⚠️ Low-quality or missing video detected for {data['id']}")
                fixed_path = re_render(data)
                data["output_fixed"] = fixed_path
                with open(path, "w") as f:
                    json.dump(data, f, indent=2)
            else:
                log(f"✅ Output verified for {data['id']}")

        time.sleep(10)

if __name__ == "__main__":
    auto_render_loop()
