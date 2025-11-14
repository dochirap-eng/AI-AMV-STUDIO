#!/usr/bin/env python3
# === AI-AMV-STUDIO — Ultra Task Monitor ===
# Fast, crash-proof, Termux optimized, auto-cleanup

import os, json, time
from flask import Flask, jsonify, send_file

ROOT = os.path.expanduser("~/AI-AMV-STUDIO")
TEMP = os.path.join(ROOT, "storage/temp")
OUTPUT = os.path.join(ROOT, "storage/output")
LOGS = os.path.join(ROOT, "storage/logs")

for d in [TEMP, OUTPUT, LOGS]:
    os.makedirs(d, exist_ok=True)

app = Flask("task_monitor")

CACHE = {
    "tasks": [],
    "outputs": [],
    "last_update": 0
}

# ---------------------------------------------------
# LOG Helper
# ---------------------------------------------------
def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] 🛰️ {msg}", flush=True)

# ---------------------------------------------------
# SMART CACHE REFRESHER
# ---------------------------------------------------
def refresh_cache():
    now = time.time()
    if now - CACHE["last_update"] < 3:
        return CACHE  # return old data to reduce CPU load

    # Refresh tasks
    tasks = []
    for f in sorted(os.listdir(TEMP)):
        if f.startswith("task_") and f.endswith(".json"):
            path = os.path.join(TEMP, f)
            try:
                data = json.load(open(path, "r"))
            except:
                data = {"error": "corrupt"}
            data["_file"] = f
            tasks.append(data)

    # Refresh outputs
    outs = []
    for f in sorted(os.listdir(OUTPUT)):
        if f.lower().endswith((".mp4", ".mov", ".mkv")):
            stat = os.stat(os.path.join(OUTPUT, f))
            outs.append({
                "file": f,
                "size": stat.st_size,
                "mtime": int(stat.st_mtime)
            })

    CACHE["tasks"] = tasks
    CACHE["outputs"] = outs
    CACHE["last_update"] = now
    return CACHE

# ---------------------------------------------------
# ROUTES
# ---------------------------------------------------
@app.route("/")
def home():
    return jsonify({"service": "AI-AMV Ultra Task Monitor", "ok": True})

@app.route("/tasks")
def api_tasks():
    return jsonify(refresh_cache()["tasks"])

@app.route("/task/<taskid>")
def api_task(taskid):
    path = os.path.join(TEMP, f"{taskid}.json")
    if not os.path.exists(path):
        return jsonify({"error": "not_found"}), 404
    return send_file(path, mimetype="application/json")

@app.route("/outputs")
def api_outputs():
    return jsonify(refresh_cache()["outputs"])

@app.route("/output/<fname>")
def api_output_file(fname):
    safe = os.path.basename(fname)
    path = os.path.join(OUTPUT, safe)
    if not os.path.exists(path):
        return jsonify({"error": "not_found"}), 404
    return send_file(path, conditional=True)

@app.route("/logs/<fname>")
def api_logs(fname):
    safe = os.path.basename(fname)
    path = os.path.join(LOGS, safe)

    if not os.path.exists(path):
        return jsonify({"error": "not_found"}), 404

    try:
        with open(path, "r", errors="ignore") as f:
            data = f.readlines()[-150:]  # last 150 lines
        return "<pre>" + "".join(data) + "</pre>"
    except Exception as e:
        return jsonify({"error": "read_failed", "detail": str(e)}), 500

@app.route("/health")
def api_health():
    cache = refresh_cache()
    return jsonify({
        "ok": True,
        "task_count": len(cache["tasks"]),
        "outputs": len(cache["outputs"]),
        "timestamp": int(time.time())
    })

# ---------------------------------------------------
# START
# ---------------------------------------------------
if __name__ == "__main__":
    log("🚀 Ultra Task Monitor running on port 5050")
    app.run(host="0.0.0.0", port=5050, debug=False)
