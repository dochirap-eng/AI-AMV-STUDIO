echo "====================================="
echo "🔍 AI-AMV-STUDIO STRUCTURE CHECK"
echo "====================================="

# Main folders
for f in backend frontend storage storage/temp storage/output storage/logs; do
  if [ -d "$HOME/AI-AMV-STUDIO/$f" ]; then
    echo "✅ Folder found: $f"
  else
    echo "❌ Missing folder: $f"
  fi
done

# Core backend files
for f in backend/server.js backend/orchestrator.py backend/gemini_manager.py backend/model_pool.json; do
  if [ -f "$HOME/AI-AMV-STUDIO/$f" ]; then
    echo "✅ File found: $f"
  else
    echo "❌ Missing file: $f"
  fi
done

# Check if node_modules exists
if [ -d "$HOME/AI-AMV-STUDIO/backend/node_modules" ]; then
  echo "✅ Node modules installed"
else
  echo "⚠️ Missing node_modules (run npm install in backend)"
fi

# Check Python availability
if command -v python3 &>/dev/null; then
  echo "✅ Python3 available"
else
  echo "❌ Python3 missing"
fi

# Check FFmpeg availability
if command -v ffmpeg &>/dev/null; then
  echo "✅ FFmpeg available"
else
  echo "⚠️ FFmpeg missing"
fi

echo "====================================="
echo "✅ STRUCTURE CHECK COMPLETE"
echo "====================================="
