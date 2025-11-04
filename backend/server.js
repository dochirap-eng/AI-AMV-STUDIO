import express from "express";
import multer from "multer";
import fetch from "node-fetch";
import fs from "fs";
import path from "path";
import FormData from "form-data";
import dotenv from "dotenv";

// 🌍 Load environment variables
dotenv.config();

const app = express();
const PORT = 5000;

// 🔥 Load Hugging Face API key from .env file (safe method)
const HF_API_KEY = process.env.HF_API_KEY;

// 💾 Upload setup
const UPLOAD_DIR = "./uploads";
fs.mkdirSync(UPLOAD_DIR, { recursive: true });
const upload = multer({ dest: UPLOAD_DIR });

// 🧠 Hugging Face model endpoint
const MODEL_URL =
  "https://api-inference.huggingface.co/models/stabilityai/stable-video-diffusion-img2vid";

// 🌐 Allow CORS
app.use((req, res, next) => {
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Methods", "GET,POST");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type");
  next();
});

// 🧩 Upload + cloud processing
app.post("/upload", upload.single("file"), async (req, res) => {
  try {
    if (!req.file) return res.status(400).json({ error: "No file uploaded" });

    console.log("📤 Upload received:", req.file.originalname);

    const form = new FormData();
    form.append("file", fs.createReadStream(req.file.path));

    console.log("☁️ Sending to Hugging Face model...");

    const response = await fetch(MODEL_URL, {
      method: "POST",
      headers: { Authorization: `Bearer ${HF_API_KEY}` },
      body: form,
    });

    if (!response.ok) {
      const errText = await response.text();
      console.error("❌ HF Error:", errText);
      return res
        .status(500)
        .json({ error: "HF API Error", detail: errText });
    }

    // 💾 Output video
    const buffer = await response.arrayBuffer();
    const outputPath = path.join("outputs", `${Date.now()}-output.mp4`);
    fs.mkdirSync(path.dirname(outputPath), { recursive: true });
    fs.writeFileSync(outputPath, Buffer.from(buffer));

    console.log("✅ Video saved:", outputPath);
    return res.json({ success: true, output: outputPath });
  } catch (err) {
    console.error("Server error:", err);
    return res.status(500).json({ error: err.message });
  }
});

// ✅ Simple test route to verify server works
app.get("/", (req, res) => {
  res.send("✅ AI AMV Backend is running properly!");
});

// ✅ Termux compatible listener
app.listen(PORT, "0.0.0.0", () => {
  console.log(`🚀 AI AMV backend running on http://0.0.0.0:${PORT}`);
});
