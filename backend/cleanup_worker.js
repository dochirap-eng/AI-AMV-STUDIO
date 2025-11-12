// cleanup_worker.js — Auto Cleanup System (local + cloud ready)
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const ROOT = path.join(__dirname, "..");
const STORAGE = path.join(ROOT, "storage");
const TEMP_DIR = path.join(STORAGE, "temp");
const OUTPUT_DIR = path.join(STORAGE, "output");
const LOGS_DIR = path.join(STORAGE, "logs");

const log = (...msg) => console.log(`[${new Date().toISOString()}]`, ...msg);
const DAYS_LIMIT = 7; // days

function deleteOldFiles(dir) {
  if (!fs.existsSync(dir)) return 0;
  const now = Date.now();
  let deleted = 0;

  for (const file of fs.readdirSync(dir)) {
    const filePath = path.join(dir, file);
    try {
      const stats = fs.statSync(filePath);
      const ageDays = (now - stats.mtimeMs) / (1000 * 60 * 60 * 24);

      // skip json tasks that are still active
      if (file.startsWith("task_") && file.endsWith(".json")) {
        const data = JSON.parse(fs.readFileSync(filePath, "utf8"));
        if (["processing", "queued", "resuming"].includes(data.status)) continue;
      }

      if (ageDays > DAYS_LIMIT) {
        fs.rmSync(filePath, { recursive: true, force: true });
        deleted++;
      }
    } catch (e) {
      log("⚠️ Error deleting:", file, e.message);
    }
  }
  return deleted;
}

function cleanupOnce() {
  log("🧹 Cleanup started...");
  const tempDeleted = deleteOldFiles(TEMP_DIR);
  const outputDeleted = deleteOldFiles(OUTPUT_DIR);
  const logsDeleted = deleteOldFiles(LOGS_DIR);
  log(`✅ Cleanup done → temp:${tempDeleted}, output:${outputDeleted}, logs:${logsDeleted}`);
}

cleanupOnce();
setInterval(cleanupOnce, 24 * 60 * 60 * 1000); // run every 24h
log("♻️ Auto Cleanup Worker Running (every 24h)");
