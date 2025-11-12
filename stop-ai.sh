#!/data/data/com.termux/files/usr/bin/bash
# === AI-AMV-STUDIO — One-Click Stopper ===

echo "========================================"
echo "🛑 Stopping AI-AMV-STUDIO System..."
echo "========================================"

# Stop all running processes safely
pkill -f "node server.js" 2>/dev/null && echo "🛑 server.js stopped"
pkill -f "python3 orchestrator.py" 2>/dev/null && echo "🛑 orchestrator stopped"
pkill -f "python3 render_manager.py" 2>/dev/null && echo "🛑 render_manager stopped"
pkill -f "python3 task_monitor.py" 2>/dev/null && echo "🛑 task_monitor stopped"
pkill -f "python3 cloud_sync_manager.py" 2>/dev/null && echo "🛑 cloud_sync_manager stopped"
pkill -f "python3 auto_ai_trigger.py" 2>/dev/null && echo "🛑 auto_ai_trigger stopped"

echo "✅ All processes stopped successfully."
echo "========================================"
