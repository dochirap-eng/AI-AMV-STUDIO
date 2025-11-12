#!/bin/bash
echo "==============================================="
echo "🚀 Launching AI-AMV-STUDIO — FULL AUTO SYSTEM"
echo "==============================================="

cd ~/AI-AMV-STUDIO/backend

# Stop any old instances first
pkill -f "node server.js"
pkill -f "orchestrator.py"
pkill -f "render_manager.py"
pkill -f "task_monitor.py"
pkill -f "cloud_sync_manager.py"
pkill -f "media_optimizer.py"
pkill -f "auto_publish.py"
pkill -f "log_viewer.py"

sleep 2

# Start all systems
nohup node server.js > ~/AI-AMV-STUDIO/storage/logs/server.log 2>&1 &
nohup python3 orchestrator.py > ~/AI-AMV-STUDIO/storage/logs/orchestrator.log 2>&1 &
nohup python3 render_manager.py > ~/AI-AMV-STUDIO/storage/logs/render_manager.log 2>&1 &
nohup python3 task_monitor.py > ~/AI-AMV-STUDIO/storage/logs/task_monitor.log 2>&1 &
nohup python3 cloud_sync_manager.py > ~/AI-AMV-STUDIO/storage/logs/cloud_sync.log 2>&1 &
nohup python3 auto_publish.py > ~/AI-AMV-STUDIO/storage/logs/auto_publish.log 2>&1 &
nohup python3 media_optimizer.py > ~/AI-AMV-STUDIO/storage/logs/media_optimizer.log 2>&1 &
nohup python3 log_viewer.py > ~/AI-AMV-STUDIO/storage/logs/log_viewer.log 2>&1 &

echo "==============================================="
echo "✅ All systems launched successfully!"
echo "📍 Backend running on: http://localhost:5000"
echo "📍 Task Monitor: http://localhost:5050"
echo "📍 Log Viewer: http://localhost:5051"
echo "==============================================="
