echo "======================================="
echo " 🔍 AI-AMV-STUDIO FULL SYSTEM CHECK "
echo "======================================="

echo ""
echo "=== ✅ Backend Process Check ==="
if ps aux | grep "node server.js" | grep -v grep > /dev/null
then
  echo "✅ Backend running"
else
  echo "❌ Backend NOT running"
fi

echo ""
echo "=== ✅ Frontend Vite Check ==="
if ps aux | grep "vite" | grep -v grep > /dev/null
then
  echo "✅ Frontend running"
else
  echo "❌ Frontend NOT running"
fi

echo ""
echo "=== ✅ Backend Health Check ==="
curl -s http://localhost:5000/health || echo "❌ Health route failed"

echo ""
echo "=== ✅ Upload Test (Dummy Ping) ==="
curl -s -X POST http://localhost:5000/upload || echo "❌ Upload API not responding (no file)"

echo ""
echo "=== ✅ FFmpeg Check ==="
ffmpeg -version 2>/dev/null | head -n 2 || echo "❌ FFmpeg not installed"

echo ""
echo "=== ✅ Upload Directory Check ==="
ls -l ~/AI-AMV-STUDIO/backend/uploads 2>/dev/null || echo "❌ Upload folder missing"

echo ""
echo "=== ✅ Output Files Check ==="
ls -l ~/AI-AMV-STUDIO/backend/*.mp4 2>/dev/null || echo "❌ No output mp4 created yet"

echo ""
echo "=== ✅ Frontend Build Check ==="
if [ -d "~/AI-AMV-STUDIO/frontend/dist" ]; then
  echo "✅ dist folder exists"
else
  echo "❌ dist folder missing — frontend not built"
fi

echo ""
echo "=== ✅ Internal File Flow Test ==="
TESTFILE="/storage/emulated/0/Download/test_check.mp4"
if [ -f "$TESTFILE" ]; then
  echo "🎬 Found test file, testing upload..."
  curl -s -X POST -F "file=@$TESTFILE" http://localhost:5000/upload
else
  echo "❌ No test file found — skipping upload test"
fi

echo ""
echo "=== ✅ Disk Space Check ==="
df -h | head -n 5

echo ""
echo "=== ✅ CPU Load Check ==="
top -b -n 1 | head -n 10

echo ""
echo "✅ FULL SYSTEM CHECK COMPLETED!"
