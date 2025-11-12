#!/usr/bin/env python3
# task_monitor.py — Simple Task Monitor API (Flask)

import os, json, time
from flask import Flask, jsonify, send_file, abort

ROOT = os.path.expanduser("~/AI-AMV-STUDIO")
STORAGE = os.path.join(ROOT, "storage")
TEMP = os.path.join(STORAGE, "temp")
OUTPUT = os.path.join(STORAGE, "output")
LOGS = os.path.join(STORAGE, "logs")

os.makedirs(TEMP, exist_ok=True)
os.makedirs(OUTPUT, exist_ok=True)
os.makedirs(LOGS, exist_ok=True)

app = Flask("task_monitor")

def list_tasks():
    out = []
    for fname in sorted(os.listdir(TEMP)):
        if not fname.startswith("task_") or not fname.endswith(".json"):
            continue
        p = os.path.join(TEMP, fname)
        try:
            j = json.load(open(p, "r"))
        except Exception:
            j = {"_raw": True}
        j["_file"] = fname
        out.append(j)
    return out

@app.route("/")
def index():
    return jsonify({"service": "AI-AMV Task Monitor", "ok": True, "time": int(time.time())})

@app.route("/tasks")
def api_tasks():
    return jsonify(list_tasks())

@app.route("/tasks/<taskid>")
def api_task(taskid):
    path = os.path.join(TEMP, f"{taskid}.json")
    if not os.path.exists(path):
        return jsonify({"error": "not_found"}), 404
    try:
        return send_file(path, mimetype="application/json")
    except Exception:
        return jsonify({"error": "read_failed"}), 500

@app.route("/outputs")
def api_outputs():
    files = []
    for f in sorted(os.listdir(OUTPUT)):
        if f.endswith(".mp4") or f.endswith(".mov") or f.endswith(".mkv"):
            st = os.stat(os.path.join(OUTPUT, f))
            files.append({"file": f, "size": st.st_size, "mtime": int(st.st_mtime)})
    return jsonify(files)

@app.route("/output/<fname>")
def api_output_file(fname):
    safe = os.path.basename(fname)
    p = os.path.join(OUTPUT, safe)
    if not os.path.exists(p): return jsonify({"error":"not_found"}), 404
    return send_file(p, conditional=True)

@app.route("/logs/<name>")
def api_log_tail(name):
    safe = os.path.basename(name)
    p = os.path.join(LOGS, safe)
    if not os.path.exists(p): return jsonify({"error":"not_found"}), 404

    # return last 200 lines (lightweight)
    try:
        with open(p, "r", errors="ignore") as f:
            lines = f.readlines()[-200:]
        return "<pre>{}</pre>".format("".join(lines)), 200, {"Content-Type": "text/html; charset=utf-8"}
    except Exception as e:
        return jsonify({"error":"read_failed", "detail": str(e)}), 500

@app.route("/health")
def health():
    ok = {"ok": True, "temp_count": len([f for f in os.listdir(TEMP) if f.endswith(".json")]),
          "outputs": len([f for f in os.listdir(OUTPUT) if f.endswith(".mp4")]),
          "time": int(time.time())}
    return jsonify(ok)

if __name__ == "__main__":
    # run on port 5050 so it doesn't clash with backend
    app.run(host="0.0.0.0", port=5050, debug=False)
