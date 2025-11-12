#!/bin/bash
echo "========================================"
echo " 🔁 FULL SYSTEM RESTART — AI-AMV-STUDIO "
echo "========================================"

# Kill running processes
echo "🛑 Stopping all running processes..."
pkill -f "node server.js"
pkill -f "python3 .*orchestrator.py"
pkill -f "python3 .*gemini_manager.py"
pkill -f "node cleanup_worker.js"
pkill -f "node resume_worker.js"
pkill -f "node cloud_backup_worker.js"
pkill -f "node cloud_restore_worker.js"
sleep 2

# Start Backend
echo "🚀 Starting Backend..."
cd ~/AI-AMV-STUDIO/backend
nohup node server.js > ~/AI-AMV-STUDIO/storage/logs/backend_restart.log 2>&1 &

# Start Orchestrator
echo "🧠 Starting Boss AI (orchestrator)..."
nohup python3 orchestrator.py > ~/AI-AMV-STUDIO/storage/logs/orchestrator_restart.log 2>&1 &

# Start Gemini Manager
echo "🔍 Starting Gemini Manager..."
nohup python3 gemini_manager.py > ~/AI-AMV-STUDIO/storage/logs/gemini_restart.log 2>&1 &

# Start Workers
echo "🧹 Starting Cleanup Worker..."
nohup node cleanup_worker.js > ~/AI-AMV-STUDIO/storage/logs/cleanup_restart.log 2>&1 &
echo "♻️ Starting Resume Worker..."
nohup node resume_worker.js > ~/AI-AMV-STUDIO/storage/logs/resume_restart.log 2>&1 &
echo "☁️ Starting Cloud Backup Worker..."
nohup node cloud_backup_worker.js > ~/AI-AMV-STUDIO/storage/logs/cloud_backup_restart.log 2>&1 &
echo "☁️ Starting Cloud Restore Worker..."
nohup node cloud_restore_worker.js > ~/AI-AMV-STUDIO/storage/logs/cloud_restore_restart.log 2>&1 &

echo "========================================"
echo "✅ All systems restarted successfully!"
echo "📄 Logs stored in: ~/AI-AMV-STUDIO/storage/logs"
echo "========================================"
