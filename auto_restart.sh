#!/bin/bash
# ============================================
# ♻️ AI-AMV-STUDIO Auto-Restart System
# ============================================

LOG_DIR=~/AI-AMV-STUDIO/storage/logs
BACKEND_DIR=~/AI-AMV-STUDIO/backend
CHECK_INTERVAL=30  # seconds

while true; do
    echo "🔍 Checking AI-AMV-STUDIO system health..."

    declare -A PROCESSES=(
        ["server.js"]="node"
        ["orchestrator.py"]="python3"
        ["render_manager.py"]="python3"
        ["task_monitor.py"]="python3"
        ["cloud_sync_manager.py"]="python3"
        ["health_monitor.py"]="python3"
        ["log_viewer.py"]="python3"
    )

    for FILE in "${!PROCESSES[@]}"; do
        PROCESS="${PROCESSES[$FILE]}"
        if ! pgrep -f "$FILE" > /dev/null; then
            echo "⚠️  $FILE not running — restarting..."
            cd $BACKEND_DIR
            nohup $PROCESS $FILE >> $LOG_DIR/${FILE%.py}.log 2>&1 &
        fi
    done

    echo "✅ System check complete — sleeping for $CHECK_INTERVAL seconds..."
    echo "---------------------------------------------"
    sleep $CHECK_INTERVAL
done
