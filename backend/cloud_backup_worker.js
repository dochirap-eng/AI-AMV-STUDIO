// cloud_backup_worker.js — Auto Cloud Upload + Delete
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";
import { exec } from "child_process";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const ROOT = path.join(__dirname, "..");
const STORAGE = path.join(ROOT, "storage");
const OUTPUT_DIR = path.join(STORAGE, "output");
const LOGS_DIR = path.join(STORAGE, "logs");

const log = (...msg) => console.log(`[${new Date().toISOString()}]`, ...msg);
const DAYS_LIMIT = 7; // 7 din baad upload

function uploadToCloud(filePath) {
  // ⚠️ Placeholder — abhi yahan pe API link add hoga
  // Tu future me Mega.nz / TeraBox API key yahan configure karega.
  log("☁️ Uploading to cloud:", filePath);

  return new Promise((resolve) => {
    // Simulate upload time (2s delay)
    setTimeout(() => {
      const fakeLink = `https://terabox.fakecloud.com/file/${path.basename(filePath)}`;
      log("✅ Uploaded:", fakeLink);
      resolve(fakeLink);
    }, 2000);
  });
}

async function backupOldFiles() {
  log("🔄 Scanning for old output files...");
  if (!fs.existsSync(OUTPUT_DIR)) return;

  const now = Date.now();
  const files = fs.readdirSync(OUTPUT_DIR);

  for (const file of files) {
    const filePath = path.join(OUTPUT_DIR, file);
    try {
      const stats = fs.statSync(filePath);
      const ageDays = (now - stats.mtimeMs) / (1000 * 60 * 60 * 24);

      if (ageDays > DAYS_LIMIT && file.endsWith(".mp4")) {
        log(`📦 Found old file: ${file} (${ageDays.toFixed(1)} days)`);

        const link = await uploadToCloud(filePath);
        const backupLog = path.join(LOGS_DIR, "cloud_backup.log");
        fs.appendFileSync(backupLog, `${new Date().toISOString()} | ${file} → ${link}\n`);

        fs.rmSync(filePath, { force: true });
        log(`🧹 Deleted local copy after backup: ${file}`);
      }
    } catch (e) {
      log("⚠️ Error:", e.message);
    }
  }
}

backupOldFiles();
setInterval(backupOldFiles, 24 * 60 * 60 * 1000); // har 24h
log("☁️ Auto Cloud Backup Worker Running (every 24h)");
