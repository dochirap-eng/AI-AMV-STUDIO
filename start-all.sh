#!/data/data/com.termux/files/usr/bin/bash
# =======================================
# 🚀 AI-AMV-STUDIO — Auto Start Script
# =======================================

ROOT=~/AI-AMV-STUDIO
BACKEND=$ROOT/backend
STORAGE=$ROOT/storage
LOGS=$STORAGE/logs

# Ensure folders exist
mkdir -p "$LOGS" "$STORAGE/temp" "$STORAGE/output"

echo "======================================="
echo " 🔥 STARTING AI-AMV-STUDIO SYSTEM "
echo "======================================="

# Stop any old processes
echo "🧹 Cleaning old sessions..."
pkill -f "node $BACKEND/server.js" 2>/dev/null
pkill -f "python3 $BACKEND/orchestrator.py" 2>/dev/null
sleep 1

# Start backend
echo "🚀 Starting Backend Server..."
nohup node "$BACKEND/server.js" > "$LOGS/backend.out" 2>&1 &

# Start Orchestrator (Boss AI)
echo "🧠 Starting Boss AI (Orchestrator)..."
nohup python3 "$BACKEND/orchestrator.py" > "$LOGS/orchestrator.out" 2>&1 &

# Start Health Monitor
echo "🩺 Health monitor activated..."
(
  while true; do
    curl -s http://localhost:5000/health >/dev/null || echo "⚠️ Backend down $(date)" >> "$LOGS/health.log"
    sleep 10
  done
) &

echo "======================================="
echo "✅ All systems started successfully!"
echo "📁 Logs: $LOGS"
echo "======================================="
