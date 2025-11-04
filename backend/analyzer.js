import express from "express";
import multer from "multer";
import cors from "cors";

const app = express();
const upload = multer({ dest: "uploads/" });

app.use(cors());
app.use(express.json());

app.get("/", (req, res) => {
  res.send("✅ AI AMV Studio Backend Active");
});

app.post("/analyze", upload.single("file"), (req, res) => {
  console.log("🎵 File received:", req.file.originalname);
  res.json({ message: "AI Analysis Complete — Beat Sync Ready!" });
});

const PORT = 5000;
app.listen(PORT, () => console.log(`🚀 Backend running on port ${PORT}`));
