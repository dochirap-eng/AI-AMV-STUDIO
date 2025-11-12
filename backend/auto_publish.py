import os, time, json, shutil

OUTPUT = os.path.expanduser("~/AI-AMV-STUDIO/storage/output")
QUEUE = os.path.expanduser("~/AI-AMV-STUDIO/storage/upload_queue")

os.makedirs(QUEUE, exist_ok=True)

def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] 🚀 {msg}", flush=True)

def move_to_queue():
    files = [f for f in os.listdir(OUTPUT) if f.endswith(".mp4")]
    for f in files:
        src = os.path.join(OUTPUT, f)
        dst = os.path.join(QUEUE, f)
        if not os.path.exists(dst):
            shutil.copy(src, dst)
            log(f"🎥 Added to upload queue: {f}")

def run_auto_publish():
    log("Auto Publish System active...")
    while True:
        move_to_queue()
        time.sleep(20)

if __name__ == "__main__":
    run_auto_publish()
