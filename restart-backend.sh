#!/bin/bash
echo "========================================"
echo " 🔁 Restarting AI-AMV-STUDIO Backend..."
echo "========================================"
# Kill existing server
pkill -f "node server.js"
sleep 2
# Start new one
cd ~/AI-AMV-STUDIO/backend
nohup node server.js > ~/AI-AMV-STUDIO/storage/logs/backend_restart.log 2>&1 &
echo "✅ Backend restarted successfully!"
echo "📄 Logs: ~/AI-AMV-STUDIO/storage/logs/backend_restart.log"
echo "========================================"
