import os, time, subprocess

OUTPUT = os.path.expanduser("~/AI-AMV-STUDIO/storage/output")
TEMP = os.path.expanduser("~/AI-AMV-STUDIO/storage/temp")

def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] 🧹 {msg}", flush=True)

def compress_video(path):
    compressed = path.replace(".mp4", "_compressed.mp4")
    subprocess.call(f"ffmpeg -i {path} -vcodec libx264 -crf 28 -preset veryfast -y {compressed}", shell=True)
    log(f"✅ Compressed: {os.path.basename(compressed)}")

def cleanup_temp():
    for f in os.listdir(TEMP):
        if f.endswith(".json") or f.endswith(".mp4"):
            os.remove(os.path.join(TEMP, f))
    log("🗑️ Temp folder cleaned.")

def auto_optimize():
    log("Media Optimizer started...")
    while True:
        for f in os.listdir(OUTPUT):
            if f.endswith(".mp4") and not f.endswith("_compressed.mp4"):
                compress_video(os.path.join(OUTPUT, f))
        cleanup_temp()
        time.sleep(60)

if __name__ == "__main__":
    auto_optimize()
