import os, time, subprocess, signal
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LOGS = ROOT / "storage" / "logs"
LOGS.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOGS / "auto_restart_guard.log"

SERVICES = {
    "Backend":  "node backend/server.js",
    "Orchestrator": "python3 backend/orchestrator.py",
    "Gemini": "python3 backend/gemini_manager.py",
    "Render": "python3 backend/render_fusion_engine.py"
}

def log(msg):
    ts = time.strftime("[%Y-%m-%d %H:%M:%S]")
    line = f"{ts} {msg}"
    print(line)
    with open(LOG_FILE, "a") as f: f.write(line + "\n")

def is_running(process_name):
    try:
        out = subprocess.check_output(["pgrep", "-f", process_name]).decode().strip()
        return bool(out)
    except subprocess.CalledProcessError:
        return False

def restart_service(name, cmd):
    log(f"⚠️  {name} crashed — restarting...")
    subprocess.Popen(cmd, shell=True)
    log(f"✅  {name} restarted successfully.")

def main():
    log("🛡️  Auto Restart Guard started (loop every 60 s)")
    while True:
        for name, cmd in SERVICES.items():
            if not is_running(cmd.split()[1]):  # basic keyword check
                restart_service(name, cmd)
        time.sleep(60)

if __name__ == "__main__":
    main()
