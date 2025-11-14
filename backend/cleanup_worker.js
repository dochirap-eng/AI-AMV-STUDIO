// ========================================================
//  AI-AMV-STUDIO — Ultra Smart Cleanup Engine (v2.0)
//  Protects active tasks, trims logs, removes junk safely
// ========================================================

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

// Retention rules
const KEEP_DAYS = 7;          // keep recent files
const MAX_LOG_LINES = 5000;   // trim logs
const KEEP_OUTPUT_LIMIT = 40; // keep last 40 renders

// ---------------------------
// LOG SYSTEM
// ---------------------------
function log(msg) {
  console.log(`[${new Date().toISOString()}] 🧹 ${msg}`);
}

// ---------------------------
// DELETE OLD FILES SAFELY
// ---------------------------
function deleteIfOld(filePath, daysLimit) {
  try {
    const stats = fs.statSync(filePath);
    const ageDays = (Date.now() - stats.mtimeMs) / (1000 * 60 * 60 * 24);

    if (ageDays > daysLimit) {
      fs.rmSync(filePath, { recursive: true, force: true });
      return true;
    }
  } catch (e) {}
  return false;
}

// ---------------------------
// CLEAN TEMP FOLDER
// ---------------------------
function cleanTemp() {
  if (!fs.existsSync(TEMP_DIR)) return;

  let deleted = 0;
  for (const file of fs.readdirSync(TEMP_DIR)) {
    const filePath = path.join(TEMP_DIR, file);

    // JSON tasks but check status to avoid deleting active tasks
    if (file.startsWith("task_") && file.endsWith(".json")) {
      try {
        const data = JSON.parse(fs.readFileSync(filePath));
        if (["processing", "queued"].includes(data.status)) continue;
      } catch {}
    }

    if (deleteIfOld(filePath, KEEP_DAYS)) deleted++;
  }
  return deleted;
}

// ---------------------------
// CLEAN OUTPUT (KEEP LATEST 40 FILES)
// ---------------------------
function cleanOutput() {
  if (!fs.existsSync(OUTPUT_DIR)) return;

  const files = fs.readdirSync(OUTPUT_DIR)
    .filter(f => f.endsWith(".mp4") || f.endsWith(".mov") || f.endsWith(".mkv"))
    .map(f => path.join(OUTPUT_DIR, f))
    .sort((a, b) => fs.statSync(a).mtimeMs - fs.statSync(b).mtimeMs); // oldest first

  let deleted = 0;

  while (files.length > KEEP_OUTPUT_LIMIT) {
    const file = files.shift();
    fs.rmSync(file, { force: true });
    deleted++;
  }

  return deleted;
}

// ---------------------------
// TRIM LOG FILES
// ---------------------------
function trimLogs() {
  if (!fs.existsSync(LOGS_DIR)) return;

  let trimmed = 0;

  for (const file of fs.readdirSync(LOGS_DIR)) {
    const filePath = path.join(LOGS_DIR, file);

    try {
      const lines = fs.readFileSync(filePath, "utf-8").split("\n");
      if (lines.length > MAX_LOG_LINES) {
        const newData = lines.slice(-MAX_LOG_LINES).join("\n");
        fs.writeFileSync(filePath, newData);
        trimmed++;
      }
    } catch {}
  }

  return trimmed;
}

// ---------------------------
// MAIN CLEANUP FUNCTION
// ---------------------------
function runCleanup() {
  log("Cleanup started...");

  const t = cleanTemp();
  const o = cleanOutput();
  const l = trimLogs();

  log(`✔ Cleanup complete → temp:${t}, output:${o}, logs_trimmed:${l}`);
}

// Run immediately and then every 12 hours
runCleanup();
setInterval(runCleanup, 12 * 60 * 60 * 1000);

log("♻ Smart Cleanup Worker running every 12 hours.");
