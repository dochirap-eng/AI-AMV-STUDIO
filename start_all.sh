#!/bin/bash
echo "========================================"
echo "🚀 Starting AI-AMV-STUDIO System..."
echo "========================================"

cd ~/AI-AMV-STUDIO/backend

# Start all backend components in background mode
nohup node server.js > ~/AI-AMV-STUDIO/storage/logs/server.log 2>&1 &
sleep 2
nohup python3 orchestrator.py > ~/AI-AMV-STUDIO/storage/logs/orchestrator.log 2>&1 &
sleep 2
nohup python3 render_manager.py > ~/AI-AMV-STUDIO/storage/logs/render_manager.log 2>&1 &
sleep 2
nohup python3 task_monitor.py > ~/AI-AMV-STUDIO/storage/logs/task_monitor.log 2>&1 &
sleep 2
nohup python3 cloud_sync_manager.py > ~/AI-AMV-STUDIO/storage/logs/cloud_sync.log 2>&1 &
sleep 2
nohup python3 health_monitor.py > ~/AI-AMV-STUDIO/storage/logs/health_monitor.log 2>&1 &
sleep 2
nohup python3 log_viewer.py > ~/AI-AMV-STUDIO/storage/logs/log_viewer.log 2>&1 &

echo "✅ All processes started successfully!"
echo "========================================"
