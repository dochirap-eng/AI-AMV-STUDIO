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

// 🔥 Load Hugging Face API key from .env file (safe method)
const HF_API_KEY = process.env.HF_API_KEY;

// 💾 Upload setup
const UPLOAD_DIR = "./uploads";
// Ensure uploads directory exists relative to the backend folder
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

// **********************************************
// ********* Zaroori Frontend Fix Code **********
// **********************************************

// 1. Static files (CSS/JS/Images) ko serve karo
// Path to the frontend build directory (from /AI-AMV-STUDIO/backend to /AI-AMV-STUDIO/frontend/dist)
const frontendPath = path.join(__dirname, '..', 'frontend', 'dist');
console.log(`Serving static files from: ${frontendPath}`);
app.use(express.static(frontendPath));

// **********************************************
// **********************************************

// 🧩 Upload + cloud processing
app.post("/upload", upload.single("file"), async (req, res) => {
  try {
    if (!req.file) return res.status(400).json({ error: "No file uploaded" });

    console.log("📤 Upload received:", req.file.originalname);

    const form = new FormData();
    // Using path.resolve to ensure correct file path in Render environment
    form.append("file", fs.createReadStream(path.resolve(req.file.path))); 

    console.log("☁️ Sending to Hugging Face model...");

    const response = await fetch(MODEL_URL, {
      method: "POST",
      headers: { Authorization: `Bearer ${HF_API_KEY}` },
      body: form,
    });

    if (!response.ok) {
      const errText = await response.text();
      console.error("❌ HF Error:", errText);
      return res.status(500).json({ error: "HF API Error", detail: errText });
    }

    // ... (rest of the output video processing code was omitted here)
    // Assuming the rest of the file response handling logic will follow here.

    // Temporary success response to keep the server working
    res.status(200).json({ message: "File uploaded and sent to Hugging Face (response part omitted for brevity).", filename: req.file.originalname });


  } catch (error) {
    console.error("🔥 Server Error:", error);
    res.status(500).json({ error: "Internal Server Error" });
  } finally {
    // Cleanup the uploaded file to save space
    if (req.file && fs.existsSync(req.file.path)) {
      fs.unlink(req.file.path, (err) => {
        if (err) console.error("Error cleaning up file:", err);
      });
    }
  }
});


// **********************************************
// ********* Zaroori Frontend Fix Code **********
// **********************************************

// 2. Catch-all route for React app (jo bhi request aaye, index.html bhej do)
// Yahaan se aapka React app serve hoga
app.get('*', (req, res) => {
    // Sirf API routes ko chhod kar, baaki sab requests ko index.html par redirect karo
    if (req.path.startsWith('/api')) {
        return; // API calls ko Express handle karega
    }
    res.sendFile(path.join(frontendPath, 'index.html'));
});

// **********************************************
// **********************************************


// ZAROORI: Port ko hamesha environment variable se uthaao
const PORT = process.env.PORT || 8080; 

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
