#!/usr/bin/env python3
# === AI-AMV-STUDIO Health Monitor (Termux Safe) ===

import os, time, psutil

def clear():
    os.system("clear" if os.name == "posix" else "cls")

def header():
    print("="*45)
    print("🧠  AI-AMV-STUDIO — REAL-TIME SYSTEM HEALTH")
    print("="*45)

def list_processes():
    print("\n⚙️  Running Processes:")
    keywords = [
        "server.js", "orchestrator.py", "render_manager.py",
        "task_monitor.py", "cloud_sync_manager.py", "auto_ai_trigger.py"
    ]
    found = False
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            cmd = " ".join(proc.info['cmdline'])
            for k in keywords:
                if k in cmd:
                    print(f"  ✅ {k} (PID {proc.info['pid']})")
                    found = True
        except:
            pass
    if not found:
        print("  ❌ No active AI-AMV-STUDIO processes found.")

def show_stats():
    print("\n💻 System Stats:")
    try:
        cpu = psutil.cpu_percent(interval=0.5)
        mem = psutil.virtual_memory().percent
        print(f"   CPU Usage: {cpu}%")
        print(f"   RAM Usage: {mem}%")
    except PermissionError:
        print("   ⚠️ CPU data unavailable (restricted by Termux)")
        print(f"   RAM Usage: {psutil.virtual_memory().percent}%")

def show_storage():
    output_dir = os.path.expanduser("~/AI-AMV-STUDIO/storage/output")
    files = os.listdir(output_dir)
    print(f"\n🎬 Output Files: {len(files)}")
    for f in files[-5:]:
        print("  🎥", f)

def monitor_loop():
    while True:
        clear()
        header()
        list_processes()
        show_stats()
        show_storage()
        print("\n⏳ Refreshing in 5s... (CTRL+C to exit)")
        time.sleep(5)

if __name__ == "__main__":
    monitor_loop()
