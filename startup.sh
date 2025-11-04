#!/data/data/com.termux/files/usr/bin/bash
# === AI AMV STUDIO AUTO START SCRIPT ===
# Yeh script backend + frontend dono ko PM2 se background mein stable run karta hai

echo "🚀 Starting AI AMV Studio..."

# Stop any existing processes (safe cleanup)
pm2 delete ai-backend >/dev/null 2>&1
pm2 delete ai-frontend >/dev/null 2>&1

# Start Backend
cd ~/AI-AMV-STUDIO/backend || exit
echo "🔧 Starting Backend..."
pm2 start analyzer.js --name ai-backend --watch --restart-delay=3000 --time

# Start Frontend
cd ~/AI-AMV-STUDIO/frontend || exit
echo "🎨 Starting Frontend..."
pm2 start "npm run dev" --name ai-frontend --cwd ~/AI-AMV-STUDIO/frontend --watch --restart-delay=3000 --time

# Save PM2 process list
pm2 save

# Display running apps
pm2 list

echo "✅ AI AMV Studio backend & frontend running in background!"
echo "Use: pm2 logs ai-backend OR pm2 logs ai-frontend to see logs"
