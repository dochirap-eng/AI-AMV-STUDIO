// dashboard.js — enhanced live task monitor (Render-ready)
const API_BACKEND = "https://ai-amv-studio.onrender.com"; // <- set your Render backend URL
const API_MONITOR = API_BACKEND; // task monitor routes fallback to same backend (Render safe)

const statusBox = document.getElementById("systemStatus");
const refreshBtn = document.getElementById("refreshStatus");

async function safeFetchJson(url) {
  try {
    const res = await fetch(url, { cache: "no-store" });
    if (!res.ok) return null;
    return await res.json();
  } catch {
    return null;
  }
}

async function fetchStatus() {
  statusBox.innerHTML = "⏳ Checking system status...";
  try {
    const [statusRes, tasksRes, outputsRes] = await Promise.all([
      safeFetchJson(`${API_BACKEND}/status`),
      safeFetchJson(`${API_MONITOR}/tasks`),
      safeFetchJson(`${API_MONITOR}/outputs`)
    ]);

    const tasks = Array.isArray(tasksRes) ? tasksRes.length : (tasksRes && tasksRes.count) || 0;
    const outputs = Array.isArray(outputsRes) ? outputsRes.length : (outputsRes && outputsRes.count) || (statusRes ? statusRes.outputs || 0 : 0);
    const uptime = statusRes && statusRes.uptime_seconds ? (statusRes.uptime_seconds / 60).toFixed(1) : "—";

    statusBox.innerHTML = `
      <div class="status-card"><h3>⚙️ Backend</h3><p>${statusRes && statusRes.backend === "running" ? "✅ Running" : "❌ Stopped"}</p></div>
      <div class="status-card"><h3>🧠 FFmpeg</h3><p>${statusRes && statusRes.ffmpeg === "installed" ? "✅ Installed" : "⚠️ Unknown"}</p></div>
      <div class="status-card"><h3>📂 Tasks</h3><p>${tasks} active</p></div>
      <div class="status-card"><h3>🎞️ Outputs</h3><p>${outputs} videos</p></div>
      <div class="status-card"><h3>⏱️ Uptime</h3><p>${uptime} mins</p></div>
    `;
  } catch (e) {
    statusBox.innerHTML = `<p style="color:red">❌ Failed to load status</p>`;
    console.error("fetchStatus error:", e);
  }
}

refreshBtn.addEventListener("click", fetchStatus);
setInterval(fetchStatus, 10000);
fetchStatus();
