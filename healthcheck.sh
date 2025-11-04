#!/data/data/com.termux/files/usr/bin/bash
# 🩺 AI AMV Studio Health Check Script

LOG_FILE="$HOME/AI-AMV-STUDIO/health_log.txt"

echo "[$(date)] 🩺 Health Check Running..." >> "$LOG_FILE"

# Check backend
if ! pm2 list | grep -q "ai-backend.*online"; then
  echo "[$(date)] ❌ Backend down! Restarting..." >> "$LOG_FILE"
  pm2 restart ai-backend
else
  echo "[$(date)] ✅ Backend OK" >> "$LOG_FILE"
fi

# Check frontend
if ! pm2 list | grep -q "ai-frontend.*online"; then
  echo "[$(date)] ❌ Frontend down! Restarting..." >> "$LOG_FILE"
  pm2 restart ai-frontend
else
  echo "[$(date)] ✅ Frontend OK" >> "$LOG_FILE"
fi
