// dashboard.js — enhanced live task monitor
const API_BACKEND = "http://localhost:5000";
const API_MONITOR = "http://localhost:5050";

const statusBox = document.getElementById("systemStatus");
const refreshBtn = document.getElementById("refreshStatus");

async function fetchStatus() {
  statusBox.innerHTML = "⏳ Checking system status...";
  try {
    const [statusRes, tasksRes, outputsRes] = await Promise.all([
      fetch(`${API_BACKEND}/status`).then(r => r.json()).catch(() => ({})),
      fetch(`${API_MONITOR}/tasks`).then(r => r.json()).catch(() => []),
      fetch(`${API_MONITOR}/outputs`).then(r => r.json()).catch(() => [])
    ]);

    const tasks = Array.isArray(tasksRes) ? tasksRes.length : 0;
    const outputs = Array.isArray(outputsRes) ? outputsRes.length : 0;
    const uptime = statusRes.uptime_seconds ? (statusRes.uptime_seconds / 60).toFixed(1) : "—";

    statusBox.innerHTML = `
      <div class="status-card"><h3>⚙️ Backend</h3><p>${statusRes.backend === "running" ? "✅ Running" : "❌ Stopped"}</p></div>
      <div class="status-card"><h3>🧠 Gemini</h3><p>${statusRes.ffmpeg === "installed" ? "✅ Active" : "⚠️ Missing"}</p></div>
      <div class="status-card"><h3>📂 Tasks</h3><p>${tasks} active</p></div>
      <div class="status-card"><h3>🎞️ Outputs</h3><p>${outputs} videos</p></div>
      <div class="status-card"><h3>⏱️ Uptime</h3><p>${uptime} mins</p></div>
    `;
  } catch (e) {
    statusBox.innerHTML = `<p style="color:red">❌ Failed to load status</p>`;
  }
}

refreshBtn.addEventListener("click", fetchStatus);
setInterval(fetchStatus, 10000);
fetchStatus();
