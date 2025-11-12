#!/usr/bin/env python3
# auto_ai_trigger.py — links orchestrator + render_manager + cloud_sync

import os, time, subprocess, signal

ROOT = os.path.expanduser("~/AI-AMV-STUDIO/backend")
LOGS = os.path.expanduser("~/AI-AMV-STUDIO/storage/logs")
os.makedirs(LOGS, exist_ok=True)

processes = {}

def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] 🤖 {msg}", flush=True)

def start_process(name, cmd):
    if name in processes and processes[name].poll() is None:
        log(f"⚠️ {name} already running.")
        return
    log(f"🚀 Starting {name} ...")
    p = subprocess.Popen(cmd, shell=True, preexec_fn=os.setsid)
    processes[name] = p

def stop_all():
    log("🛑 Stopping all processes...")
    for name, p in processes.items():
        try:
            os.killpg(os.getpgid(p.pid), signal.SIGTERM)
        except:
            pass
    log("✅ All stopped.")

def auto_loop():
    log("🤖 AUTO-AI Trigger System started.")
    start_process("server", f"node {ROOT}/server.js")
    time.sleep(3)
    start_process("orchestrator", f"python3 {ROOT}/orchestrator.py")
    time.sleep(2)
    start_process("render_manager", f"python3 {ROOT}/render_manager.py")
    time.sleep(2)
    start_process("task_monitor", f"python3 {ROOT}/task_monitor.py")
    time.sleep(2)
    start_process("cloud_sync", f"python3 {ROOT}/cloud_sync_manager.py")

    while True:
        for name, p in processes.items():
            if p.poll() is not None:
                log(f"⚠️ {name} crashed! restarting...")
                if name == "server":
                    start_process(name, f"node {ROOT}/server.js")
                elif name == "orchestrator":
                    start_process(name, f"python3 {ROOT}/orchestrator.py")
                elif name == "render_manager":
                    start_process(name, f"python3 {ROOT}/render_manager.py")
                elif name == "task_monitor":
                    start_process(name, f"python3 {ROOT}/task_monitor.py")
                elif name == "cloud_sync":
                    start_process(name, f"python3 {ROOT}/cloud_sync_manager.py")
        time.sleep(10)

if __name__ == "__main__":
    try:
        auto_loop()
    except KeyboardInterrupt:
        stop_all()
        log("👋 Exiting Auto-AI Trigger System.")
