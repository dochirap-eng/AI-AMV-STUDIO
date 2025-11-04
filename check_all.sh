#!/data/data/com.termux/files/usr/bin/bash
set -e

echo "===== AI AMV STUDIO - QUICK DIAGNOSTICS ====="
echo

# 1) PM2 status
echo "-> PM2 process list (if installed):"
if command -v pm2 >/dev/null 2>&1; then
  pm2 list || echo "pm2 list failed"
else
  echo "pm2 not installed"
fi
echo

# 2) Node processes
echo "-> Node / npm processes (ps aux | grep node):"
ps aux | grep node | grep -v grep || echo "(no node processes found)"
echo

# 3) Backend health
BACKEND_DIR=~/AI-AMV-STUDIO/backend
BACKEND_FILE="$BACKEND_DIR/server.js"
echo "-> Backend file check: $BACKEND_FILE"
if [ -f "$BACKEND_FILE" ]; then
  echo "  exists: $BACKEND_FILE"
else
  echo "  MISSING: $BACKEND_FILE"
fi

echo "-> Backend HTTP health check (http://127.0.0.1:5000/):"
if command -v curl >/dev/null 2>&1; then
  curl -sS --max-time 5 http://127.0.0.1:5000/ && echo || echo "No response from backend (timeout or not running)"
else
  echo "curl not installed"
fi
echo

# 4) Frontend server check (vite or python http)
FRONTEND_DIR=~/AI-AMV-STUDIO/frontend
echo "-> Frontend folder:"
ls -la "$FRONTEND_DIR" 2>/dev/null || echo "frontend folder not found"
echo

echo "-> Check frontend live URLs (common ports 5173 vite, 8080 python):"
for P in 5173 5174 5175 8080; do
  if command -v curl >/dev/null 2>&1; then
    echo -n "  http://127.0.0.1:$P -> "
    curl -s --max-time 3 "http://127.0.0.1:$P/" | head -c120 && echo || echo "no response"
  fi
done
echo

# 5) Ports in use (ss or netstat)
echo "-> Listening ports (ss -ltnp or netstat -ltnp):"
if command -v ss >/dev/null 2>&1; then
  ss -ltnp | head -n 40
elif command -v netstat >/dev/null 2>&1; then
  netstat -ltnp | head -n 40
else
  echo "neither ss nor netstat installed"
fi
echo

# 6) Upload folder (Termux storage)
UPLOAD_DIR=~/storage/downloads/uploads
echo "-> Upload folder check: $UPLOAD_DIR"
if [ -d "$UPLOAD_DIR" ]; then
  echo "  exists. contents:"
  ls -la "$UPLOAD_DIR" | sed -n '1,20p'
else
  echo "  missing. create now? (y/n)"
  read -r createchoice
  if [ "$createchoice" = "y" ]; then
    mkdir -p "$UPLOAD_DIR"
    echo "created $UPLOAD_DIR"
  else
    echo "skipped creating upload dir"
  fi
fi
echo

# 7) Check sample upload endpoint (try to list /files)
echo "-> Try GET /files on backend (if server exposes it):"
if command -v curl >/dev/null 2>&1; then
  curl -s --max-time 5 http://127.0.0.1:5000/files | sed -n '1,20p' || echo "(no /files response)"
else
  echo "curl not installed"
fi
echo

# 8) Check HUGGINGFACE token env (only in current shell)
echo "-> Check HUGGINGFACE_TOKEN env in this shell (NOT read from disk):"
if [ -z "$HUGGINGFACE_TOKEN" ]; then
  echo "  HUGGINGFACE_TOKEN is NOT set in this shell"
else
  echo "  HUGGINGFACE_TOKEN is set (length: ${#HUGGINGFACE_TOKEN})"
fi
echo

# 9) Tail logs (pm2 logs or simple file)
echo "-> Tail backend log (backend.log if exists) - showing last 20 lines:"
if [ -f "$BACKEND_DIR/backend.log" ]; then
  tail -n 20 "$BACKEND_DIR/backend.log"
else
  echo "  backend.log not found"
fi
echo

echo "===== Diagnostics finished ====="
