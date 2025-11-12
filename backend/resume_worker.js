// resume_worker.js
// Usage: node resume_worker.js
import fs from "fs";
import path from "path";
import { exec } from "child_process";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const ROOT = path.join(__dirname, "..");
const TEMP_DIR = path.join(ROOT, "storage", "temp");
const OUTPUT_DIR = path.join(ROOT, "storage", "output");
const LOCK_SUFFIX = ".lock";

if (!fs.existsSync(TEMP_DIR)) fs.mkdirSync(TEMP_DIR, { recursive: true });
if (!fs.existsSync(OUTPUT_DIR)) fs.mkdirSync(OUTPUT_DIR, { recursive: true });

const log = (...args) => console.log(new Date().toISOString(), ...args);

function listTaskFiles() {
  return fs.readdirSync(TEMP_DIR).filter(f => f.startsWith("task_") && f.endsWith(".json"));
}

function readTask(file) {
  try {
    const p = path.join(TEMP_DIR, file);
    return JSON.parse(fs.readFileSync(p, "utf8"));
  } catch (e) {
    return null;
  }
}

function writeTaskObj(task) {
  const p = path.join(TEMP_DIR, `${task.id}.json`);
  fs.writeFileSync(p, JSON.stringify(task, null, 2));
}

function lockTask(taskId) {
  const l = path.join(TEMP_DIR, `${taskId}${LOCK_SUFFIX}`);
  try {
    fs.writeFileSync(l, String(process.pid));
    return true;
  } catch (e) {
    return false;
  }
}

function unlockTask(taskId) {
  const l = path.join(TEMP_DIR, `${taskId}${LOCK_SUFFIX}`);
  try { if (fs.existsSync(l)) fs.unlinkSync(l); } catch (e) {}
}

function isLocked(taskId) {
  const l = path.join(TEMP_DIR, `${taskId}${LOCK_SUFFIX}`);
  return fs.existsSync(l);
}

// Basic ffmpeg process for demo: if video clips present -> concat them (if multiple) else copy input -> output
function processTask(task) {
  return new Promise((resolve) => {
    const taskPath = path.join(TEMP_DIR, `${task.id}.json`);
    log("▶️ processing:", task.id);

    // update status
    task.status = "processing";
    task.started_at = Date.now();
    writeTaskObj(task);

    // Determine input clips
    const videos = task.inputs?.videos || [];
    const audio = task.inputs?.audio || null;

    // If no videos and no audio -> fail
    if ((!videos || videos.length === 0) && !audio) {
      task.status = "failed";
      task.error = "no_inputs";
      task.finished_at = Date.now();
      writeTaskObj(task);
      unlockTask(task.id);
      return resolve(task);
    }

    // prepare output name
    const outName = `resume_${Date.now()}_${task.id}.mp4`;
    const outPath = path.join(OUTPUT_DIR, outName);

    // If multiple clips -> create concat list
    if (videos.length > 1) {
      const listFile = path.join(TEMP_DIR, `concat_${task.id}.txt`);
      const lines = videos.map(v => `file '${v.replace(/'/g, "\\'")}'`).join("\n");
      fs.writeFileSync(listFile, lines, "utf8");

      const cmd = `ffmpeg -y -f concat -safe 0 -i "${listFile}" -c copy "${outPath}"`;
      log("ffmpeg cmd:", cmd);
      exec(cmd, (err, so, se) => {
        try { fs.unlinkSync(listFile); } catch (e) {}
        if (err) {
          log("❌ ffmpeg error:", se?.slice?.(0,1000) || err.message);
          task.status = "failed";
          task.error = "ffmpeg_concat_failed";
          task.stderr = se;
        } else {
          task.status = "done";
          task.output = outPath;
        }
        task.finished_at = Date.now();
        writeTaskObj(task);
        unlockTask(task.id);
        resolve(task);
      });

    } else {
      // single file or only audio: if only audio -> create small silent video (not ideal) - here we just copy video
      const input = videos[0] || audio;
      if (!fs.existsSync(input)) {
        task.status = "failed";
        task.error = "input_missing";
        task.finished_at = Date.now();
        writeTaskObj(task);
        unlockTask(task.id);
        return resolve(task);
      }

      const cmd = `ffmpeg -y -i "${input}" -c:v libx264 -preset ultrafast -crf 28 -c:a aac "${outPath}"`;
      log("ffmpeg cmd:", cmd);
      exec(cmd, (err, so, se) => {
        if (err) {
          log("❌ ffmpeg error:", se?.slice?.(0,1000) || err.message);
          task.status = "failed";
          task.error = "ffmpeg_transcode_failed";
          task.stderr = se;
        } else {
          task.status = "done";
          task.output = outPath;
        }
        task.finished_at = Date.now();
        writeTaskObj(task);
        unlockTask(task.id);
        resolve(task);
      });
    }
  });
}

// main loop: find tasks that need resume and process them (one by one)
async function mainOnce() {
  log("🔎 Scanning for resumable tasks...");
  const files = listTaskFiles();
  for (const f of files) {
    const t = readTask(f);
    if (!t) continue;
    // statuses to resume: queued, processing, running, planned, resuming
    if (["done","failed","cancelled"].includes(t.status)) continue;
    if (isLocked(t.id)) {
      log("⏳ locked, skipping:", t.id);
      continue;
    }
    // Acquire lock
    if (!lockTask(t.id)) {
      log("⚠️ could not lock:", t.id);
      continue;
    }
    try {
      // mark resumed
      t.status = "resuming";
      t.resumed_at = Date.now();
      t.notes = t.notes || [];
      t.notes.push(`resumed_by_worker:${new Date().toISOString()}`);
      writeTaskObj(t);
      // process
      await processTask(t);
      log("✅ done handling:", t.id);
    } catch (e) {
      log("🔥 worker error:", e);
      t.status = "failed";
      t.error = String(e).slice(0,1000);
      writeTaskObj(t);
      unlockTask(t.id);
    }
  }
}

// run once at start, then schedule periodic scan
(async () => {
  try {
    await mainOnce();
    // periodic scan every 30s
    setInterval(mainOnce, 30 * 1000);
    log("🛠️ Resume worker running (scan every 30s)");
  } catch (e) {
    log("Fatal worker error:", e);
    process.exit(1);
  }
})();
