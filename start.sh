#!/bin/bash

echo "🚀 Starting AI AMV Studio..."

# 1️⃣ Kill any old processes (to avoid port errors)
pkill -f "http.server"
pkill -f "flask"
pkill -f "app.py"

# 2️⃣ Start backend (Flask app)
cd ~/AI-AMV-STUDIO/backend
nohup python3 app.py > ~/AI-AMV-STUDIO/backend.log 2>&1 &
sleep 3
echo "✅ Backend running on port 5000"

# 3️⃣ Start frontend server
cd ~/AI-AMV-STUDIO/frontend
nohup python3 -m http.server 8080 > ~/AI-AMV-STUDIO/frontend.log 2>&1 &
sleep 2
echo "🌐 Frontend running on: http://127.0.0.1:8080"

# 4️⃣ Auto open in browser
termux-open-url http://127.0.0.1:8080

echo "✅ AI AMV Studio fully started!"
