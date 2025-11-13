import time
import json
import os
import subprocess

BASE = os.path.expanduser("~/AI-AMV-STUDIO/storage")
TEMP = os.path.join(BASE, "temp")
OUTPUT = os.path.join(BASE, "output")

def safe_print(msg):
    print("[SAFE-ORCH] " + str(msg), flush=True)

def run_file(path):
    """Run a python file safely on Render"""
    try:
        safe_print("Running: " + path)
        subprocess.call(["python3", path])
    except Exception as e:
        safe_print("ERROR running " + path + " : " + str(e))

def check_pending_tasks():
    """Check number of pending tasks"""
    if not os.path.exists(TEMP):
        return 0

    files = [f for f in os.listdir(TEMP) if f.endswith(".json")]
    return len(files)

# ========== SAFE MAIN LOOP (Render compatible) ==========

safe_print("SAFE ORCHESTRATOR STARTED")

while True:
    try:
        pending = check_pending_tasks()
        safe_print("Pending tasks: " + str(pending))

        if pending > 0:
            safe_print("➡ Running orchestrator.py")
            run_file("backend/orchestrator.py")

            safe_print("➡ Running render_manager.py")
            run_file("backend/render_manager.py")
        else:
            safe_print("No tasks. Sleeping...")

        time.sleep(5)

    except Exception as e:
        safe_print("MAIN LOOP ERROR: " + str(e))
        time.sleep(5)
