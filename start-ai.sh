#!/data/data/com.termux/files/usr/bin/bash
# === AI-AMV-STUDIO — One-Click Full System Launcher ===

echo "========================================"
echo "🚀 Starting AI-AMV-STUDIO Full System..."
echo "========================================"

# ✅ Create required directories
mkdir -p ~/AI-AMV-STUDIO/storage/logs
mkdir -p ~/AI-AMV-STUDIO/storage/output
mkdir -p ~/AI-AMV-STUDIO/storage/temp
mkdir -p ~/AI-AMV-STUDIO/cloud_backup

# ✅ Stop any running Node or Python background jobs
echo "🧹 Cleaning old processes..."
pkill -f "node server.js" 2>/dev/null
pkill -f "python3 orchestrator.py" 2>/dev/null
pkill -f "python3 render_manager.py" 2>/dev/null
pkill -f "python3 task_monitor.py" 2>/dev/null
pkill -f "python3 cloud_sync_manager.py" 2>/dev/null
pkill -f "python3 auto_ai_trigger.py" 2>/dev/null

# ✅ Start Auto AI Trigger System
echo "🤖 Launching Auto-AI Trigger..."
cd ~/AI-AMV-STUDIO/backend
nohup python3 auto_ai_trigger.py > ~/AI-AMV-STUDIO/storage/logs/auto_ai_trigger.log 2>&1 &

sleep 3
echo "========================================"
echo "✅ AI-AMV-STUDIO Running Successfully!"
echo "🌐 Frontend: http://localhost:5173"
echo "⚙️ Backend API: http://localhost:5000"
echo "📊 Task Monitor: http://localhost:5050"
echo "📄 Logs: ~/AI-AMV-STUDIO/storage/logs/"
echo "========================================"
