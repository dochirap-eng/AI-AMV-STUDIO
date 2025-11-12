// cloud_restore_worker.js — Restore deleted files from cloud backup
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
const BACKUP_LOG = path.join(LOGS_DIR, "cloud_backup.log");

const log = (...msg) => console.log(`[${new Date().toISOString()}]`, ...msg);

function parseBackupLog() {
  if (!fs.existsSync(BACKUP_LOG)) return [];
  const lines = fs.readFileSync(BACKUP_LOG, "utf-8").trim().split("\n");
  return lines.map(line => {
    const [date, rest] = line.split(" | ");
    if (!rest) return null;
    const [file, url] = rest.split(" → ");
    return { file, url };
  }).filter(Boolean);
}

function downloadFile(url, destPath) {
  return new Promise((resolve, reject) => {
    log("⬇️ Restoring:", url);
    exec(`curl -L "${url}" -o "${destPath}"`, (err) => {
      if (err) reject(err);
      else resolve(destPath);
    });
  });
}

async function restoreFile(fileName) {
  const entries = parseBackupLog();
  const entry = entries.find(e => e.file === fileName);
  if (!entry) {
    log("❌ File not found in backup log:", fileName);
    return { ok: false, error: "not_found" };
  }

  const destPath = path.join(OUTPUT_DIR, fileName);
  try {
    await downloadFile(entry.url, destPath);
    log(`✅ Restored: ${fileName}`);
    return { ok: true, path: destPath };
  } catch (e) {
    log("⚠️ Restore error:", e.message);
    return { ok: false, error: e.message };
  }
}

async function autoRestoreMissing() {
  log("🔍 Checking for missing files...");
  const entries = parseBackupLog();
  if (!entries.length) return log("ℹ️ No backups found.");

  for (const e of entries) {
    const localPath = path.join(OUTPUT_DIR, e.file);
    if (!fs.existsSync(localPath)) {
      log(`♻️ Missing file detected: ${e.file}`);
      await restoreFile(e.file);
    }
  }
}

autoRestoreMissing();
setInterval(autoRestoreMissing, 12 * 60 * 60 * 1000); // har 12 ghante me check
log("☁️ Cloud Restore Worker Active (auto-check every 12h)");

export { restoreFile };
