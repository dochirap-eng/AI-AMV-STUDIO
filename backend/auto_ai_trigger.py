#!/usr/bin/env python3
# === AI-AMV-STUDIO — SUPER AI TRIGGER SYSTEM ===
# Creative Boss AI + Gemini + Workers — all controlled here

import os, time, subprocess, signal, json, psutil
from pathlib import Path

ROOT = Path(os.path.expanduser("~/AI-AMV-STUDIO/backend"))
LOGS = Path(os.path.expanduser("~/AI-AMV-STUDIO/storage/logs"))
LOGS.mkdir(parents=True, exist_ok=True)

processes = {}
HEALTH = {}
COOLDOWN = {}

def log(msg):
    stamp = time.strftime("[%H:%M:%S]")
    print(f"{stamp} 🤖 {msg}", flush=True)
    with open(LOGS / "auto_ai_trigger.log", "a") as f:
        f.write(f"{stamp} {msg}\n")

# ------------------------------------------------------
# 🔥 START PROCESS
# ------------------------------------------------------
def start_process(name, cmd):
    if name in processes and processes[name].poll() is None:
        log(f"⚠️ {name} already running.")
        return

    log(f"🚀 Starting {name} ...")
    p = subprocess.Popen(cmd, shell=True, preexec_fn=os.setsid)

    processes[name] = p
    HEALTH[name] = {"restarts": 0, "last_start": time.time()}
    COOLDOWN[name] = 0

# ------------------------------------------------------
# 🛑 STOP PROCESS
# ------------------------------------------------------
def stop_process(name):
    if name not in processes:
        return
    try:
        os.killpg(os.getpgid(processes[name].pid), signal.SIGTERM)
    except:
        pass

# ------------------------------------------------------
# 🧠 CHECK SYSTEM LOAD
# ------------------------------------------------------
def system_overloaded():
    try:
        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory().percent
        if cpu > 92 or ram > 92:
            log(f"⚠️ System overload detected (CPU={cpu} RAM={ram})")
            return True
    except:
        return False
    return False

# ------------------------------------------------------
# ♻ AUTO RESTART WITH COOLDOWN PROTECTION
# ------------------------------------------------------
def respawn(name, cmd):
    now = time.time()

    # If crashed too many times, increase cooldown
    if HEALTH[name]["restarts"] >= 3:
        if now - COOLDOWN[name] < 20:
            log(f"⏳ Cooldown active for {name}. Waiting...")
            return
        COOLDOWN[name] = now
        HEALTH[name]["restarts"] = 0

    log(f"🔥 Restarting crashed process: {name}")
    start_process(name, cmd)
    HEALTH[name]["restarts"] += 1

# ------------------------------------------------------
# 🚀 AUTO CONTROL LOOP
# ------------------------------------------------------
def auto_loop():
    log("🤖 AUTO-AI Trigger Started (Creative Brain Active)")

    start_process("server", f"node {ROOT}/server.js")
    start_process("orchestrator", f"python3 {ROOT}/orchestrator.py")
    start_process("render_manager", f"python3 {ROOT}/render_manager.py")
    start_process("task_monitor", f"python3 {ROOT}/task_monitor.py")
    start_process("cloud_sync", f"python3 {ROOT}/cloud_sync_manager.py")

    while True:
        if system_overloaded():
            log("⚠️ Auto-Reduce Load: Pausing heavy processes...")
            stop_process("render_manager")
            time.sleep(5)
            start_process("render_manager", f"python3 {ROOT}/render_manager.py")

        # Check worker crashes
        for name, p in processes.items():
            if p.poll() is not None:
                log(f"💥 {name} crashed!")
                if name == "server":
                    respawn(name, f"node {ROOT}/server.js")
                elif name == "orchestrator":
                    respawn(name, f"python3 {ROOT}/orchestrator.py")
                elif name == "render_manager":
                    respawn(name, f"python3 {ROOT}/render_manager.py")
                elif name == "task_monitor":
                    respawn(name, f"python3 {ROOT}/task_monitor.py")
                elif name == "cloud_sync":
                    respawn(name, f"python3 {ROOT}/cloud_sync_manager.py")

        time.sleep(5)

# ------------------------------------------------------
# MAIN
# ------------------------------------------------------
if __name__ == "__main__":
    try:
        auto_loop()
    except KeyboardInterrupt:
        log("🛑 Shutting down all workers...")
        for n in processes:
            stop_process(n)
        log("👋 EXIT SAFE")
