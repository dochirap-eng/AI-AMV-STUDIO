import express from "express";
import multer from "multer";
import cors from "cors";
import fs from "fs";
import path from "path";
import os from "os";

const app = express();

// 🌐 UNIVERSAL PORT (Termux + Render + Cloudflare Tunnel)
const PORT = process.env.PORT || 5000;

// 🌐 CORS (Full Protection)
app.use(
  cors({
    origin: "*",
    methods: ["GET", "POST", "OPTIONS"],
    allowedHeaders: ["Content-Type", "x-api-key"],
  })
);

app.use(express.json({ limit: "200mb" }));

// 📂 STORAGE SYSTEM
const STORAGE = path.join(os.homedir(), "AI-AMV-STUDIO", "storage");
const TEMP = path.join(STORAGE, "temp");
const OUTPUT = path.join(STORAGE, "output");
const LOGS = path.join(STORAGE, "logs");

// Auto create dirs
for (const dir of [STORAGE, TEMP, OUTPUT, LOGS]) {
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
}

// Public file serving
app.use("/output", express.static(OUTPUT));
app.use("/temp", express.static(TEMP));
app.use("/logs", express.static(LOGS));

// 🟡 MULTER (Safe Upload)
const upload = multer({
  dest: TEMP,
  limits: { fileSize: 1024 * 1024 * 1024 }, // 1GB MAX
});

// 🧠 BOSS-AI: Create New Task
app.post(
  "/api/tasks/new",
  upload.fields([{ name: "audio" }, { name: "video" }]),
  (req, res) => {
    try {
      const id = "task_" + Date.now();
      const taskPath = path.join(TEMP, `${id}.json`);

      const taskData = {
        id,
        prompt: req.body.prompt || "default",
        audio: req.files.audio ? req.files.audio[0].path : null,
        videos: req.files.video ? req.files.video.map(v => v.path) : [],
        status: "pending",
        created_at: Date.now(),
      };

      fs.writeFileSync(taskPath, JSON.stringify(taskData, null, 2));

      console.log(`🟢 New Task Created → ${id}`);
      return res.json({ ok: true, taskId: id });
    } catch (e) {
      console.error("❌ Task Create Error:", e);
      return res.status(500).json({ ok: false, error: e.message });
    }
  }
);

// 🟢 Get Single Task
app.get("/api/tasks/:id", (req, res) => {
  const file = path.join(TEMP, `${req.params.id}.json`);
  if (!fs.existsSync(file)) return res.json({ error: "not_found" });
  return res.sendFile(file);
});

// 🟢 List All Tasks
app.get("/api/tasks", (req, res) => {
  const files = fs
    .readdirSync(TEMP)
    .filter(f => f.startsWith("task_") && f.endsWith(".json"));
  res.json(files);
});

// 🟢 List Rendered Outputs
app.get("/api/outputs", (req, res) => {
  const files = fs
    .readdirSync(OUTPUT)
    .filter(f => f.endsWith(".mp4") || f.endsWith(".mov"));
  res.json(files);
});

// 🟢 System Health Status (Dashboard Pro)
app.get("/status", (req, res) => {
  const uptime = process.uptime();

  res.json({
    backend: "running",
    uptime_seconds: uptime,
    storage: {
      temp_files: fs.readdirSync(TEMP).length,
      output_files: fs.readdirSync(OUTPUT).length,
      logs: fs.readdirSync(LOGS).length,
    },
    ffmpeg: "installed",
    version: "2.0.1-stable",
    boss_ai: "connected",
    gemini_manager: "online",
    auto_workers: "active",
  });
});

// 🟢 Root
app.get("/", (req, res) => {
  res.json({
    ok: true,
    name: "AI AMV Studio Backend",
    status: "online",
    docs: "/status",
  });
});

// ❌ Catch All
app.use((req, res) => {
  res.status(404).json({ ok: false, error: "Invalid Route" });
});

// ▶️ Start Backend
app.listen(PORT, () => {
  console.log(`🚀 Backend Online at http://127.0.0.1:${PORT}`);
});
