#!/usr/bin/env python3
# === AI-AMV-STUDIO Log Viewer Panel ===

from flask import Flask, render_template_string, send_file
import os, sys

# 🧠 Port argument handling
port = 5051
if len(sys.argv) > 1:
    for arg in sys.argv:
        if arg.startswith("--port="):
            try:
                port = int(arg.split("=")[1])
            except:
                port = 5051

app = Flask(__name__)

LOG_DIR = os.path.expanduser("~/AI-AMV-STUDIO/storage/logs")

HTML_TEMPLATE = """                                                                                       
<!DOCTYPE html>
<html>
<head>
<title>🧠 AI-AMV-STUDIO — Log Viewer</title>
<style>
  body { background: #0a0a0a; color: #00ffff; font-family: monospace; padding: 20px; }
  h1 { color: #00ffff; text-align: center; }
  .log-list { margin-top: 20px; display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
  .log-item { background: rgba(255,255,255,0.1); padding: 10px; border-radius: 10px; }
  a { color: #00ffff; text-decoration: none; }
  a:hover { text-decoration: underline; }
  pre { background: #111; color: #fff; padding: 15px; border-radius: 8px; max-height: 400px; overflow-y: auto; }
</style>
</head>
<body>
  <h1>🧠 AI-AMV-STUDIO — Log Viewer</h1>
  <div class="log-list">
    {% for file in files %}
      <div class="log-item">
        <a href="/view/{{ file }}">{{ file }}</a>
      </div>
    {% endfor %}
  </div>
  <hr>
  {% if log_content %}
    <h2>📜 Viewing: {{ selected_file }}</h2>
    <pre>{{ log_content }}</pre>
  {% endif %}
</body>
</html>
"""

@app.route('/')
def index():
    files = os.listdir(LOG_DIR)
    files = sorted(files)
    return render_template_string(HTML_TEMPLATE, files=files, log_content=None, selected_file=None)

@app.route('/view/<path:filename>')
def view_log(filename):
    path = os.path.join(LOG_DIR, filename)
    if not os.path.exists(path):
        return "Log file not found.", 404
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()[-10000:]  # last 10k chars only
    files = sorted(os.listdir(LOG_DIR))
    return render_template_string(HTML_TEMPLATE, files=files, log_content=content, selected_file=filename)

@app.route('/download/<path:filename>')
def download_log(filename):
    path = os.path.join(LOG_DIR, filename)
    return send_file(path, as_attachment=True)

if __name__ == "__main__":
    print(f"🚀 Log Viewer running on http://localhost:{port}/")
    app.run(host="0.0.0.0", port=port)
