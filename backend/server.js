import express from "express";
import multer from "multer";
import cors from "cors";
import fs from "fs";
import path from "path";
import os from "os";

const app = express();

// 🔥 Render-safe PORT
const PORT = process.env.PORT || 5000;

// 🔥 CORS Fix (Vercel + Render)
app.use(
  cors({
    origin: "*",
    methods: ["GET", "POST"],
    allowedHeaders: ["Content-Type"],
  })
);

app.use(express.json());

// 🔥 STORAGE SETUP
const STORAGE = path.join(os.homedir(), "AI-AMV-STUDIO", "storage");
const TEMP = path.join(STORAGE, "temp");
const OUTPUT = path.join(STORAGE, "output");
const LOGS = path.join(STORAGE, "logs");

// Auto create folders (safe for Termux + Render)
for (const dir of [STORAGE, TEMP, OUTPUT, LOGS]) {
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
}

// Serve output + logs directories
app.use("/output", express.static(OUTPUT));
app.use("/logs", express.static(LOGS));

// Multer upload temp config
const upload = multer({ dest: TEMP });

// 🟢 Create new task
app.post(
  "/api/tasks/new",
  upload.fields([{ name: "audio" }, { name: "video" }]),
  (req, res) => {
    try {
      const id = "task_" + Date.now();
      const prompt = req.body.prompt || "default edit";
      const taskPath = path.join(TEMP, `${id}.json`);

      const taskData = {
        id,
        prompt,
        audio: req.files.audio ? req.files.audio[0].path : null,
        videos: req.files.video ? req.files.video.map(v => v.path) : [],
        status: "pending",
        created_at: new Date().toISOString(),
      };

      fs.writeFileSync(taskPath, JSON.stringify(taskData, null, 2));

      console.log(`[SERVER] ✅ Task created: ${id}`);
      res.json({ ok: true, taskId: id });
    } catch (err) {
      console.error("❌ Task creation error:", err);
      res.status(500).json({ ok: false, error: err.message });
    }
  }
);

// 🧠 System Status
app.get("/status", (req, res) => {
  const uptime_seconds = process.uptime();
  const backend = "running";
  const ffmpeg = "installed";

  const outputs = fs.existsSync(OUTPUT) ? fs.readdirSync(OUTPUT).length : 0;
  const upload_files = fs.existsSync(TEMP) ? fs.readdirSync(TEMP).length : 0;

  res.json({
    backend,
    ffmpeg,
    outputs,
    upload_files,
    uptime_seconds,
  });
});

// 🟢 List tasks (Render-safe)
app.get("/tasks", (req, res) => {
  try {
    const files = fs.readdirSync(TEMP)
      .filter(f => f.endsWith(".json"));
    res.json(files);
  } catch (e) {
    res.json([]);
  }
});

// 🟢 List outputs (Render-safe)
app.get("/outputs", (req, res) => {
  try {
    const files = fs.readdirSync(OUTPUT)
      .filter(f => f.endsWith(".mp4"));
    res.json(files);
  } catch (e) {
    res.json([]);
  }
});

// Root endpoint
app.get("/", (req, res) => {
  res.json({ ok: true, message: "AI-AMV-STUDIO Backend Online" });
});

// Catch-all endpoint
app.get("*", (req, res) => {
  res.json({ ok: false, error: "Invalid route" });
});

// 🚀 Start Server
app.listen(PORT, () => {
  console.log(`✅ Backend running on port ${PORT}`);
});
