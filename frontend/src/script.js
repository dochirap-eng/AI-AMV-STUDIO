// 🌐 AI AMV Studio Frontend Script
console.log("🚀 AI-AMV-STUDIO Frontend Ready");

const statusBox = document.getElementById("statusBox");
const startBtn = document.getElementById("startBtn");
const promptInput = document.getElementById("promptInput");
const audioFile = document.getElementById("audioFile");
const videoFiles = document.getElementById("videoFiles");
const previewBox = document.getElementById("previewBox");

async function checkStatus() {
  try {
    const res = await fetch("/status");
    const data = await res.json();
    statusBox.innerHTML =
      `🩺 <b>Backend:</b> ${data.backend} | <b>FFmpeg:</b> ${data.ffmpeg} | <b>Uploads:</b> ${data.upload_files} | <b>Outputs:</b> ${data.outputs}`;
  } catch (err) {
    statusBox.innerHTML = "❌ Backend offline!";
  }
}

async function createTask() {
  if (!audioFile.files.length) {
    alert("🎵 Please upload a song first!");
    return;
  }

  const formData = new FormData();
  formData.append("audio", audioFile.files[0]);
  for (const f of videoFiles.files) formData.append("video", f);
  formData.append("prompt", promptInput.value);

  statusBox.innerHTML = "⏳ Creating new task...";
  try {
    const res = await fetch("/api/tasks/new", {
      method: "POST",
      body: formData,
    });
    const data = await res.json();

    if (data.ok) {
      statusBox.innerHTML = `✅ Task Created — <b>${data.taskId}</b><br>🔁 Waiting for processing...`;
      pollTaskStatus(data.taskId);
    } else {
      statusBox.innerHTML = "❌ Task creation failed.";
    }
  } catch (err) {
    statusBox.innerHTML = "🔥 Upload error: " + err;
  }
}

// Live polling for task updates
async function pollTaskStatus(taskId) {
  const interval = setInterval(async () => {
    try {
      const res = await fetch(`/api/tasks/${taskId}`);
      const task = await res.json();

      if (task.status === "done" || task.status === "completed") {
        clearInterval(interval);
        statusBox.innerHTML = `🎬 Render completed!<br><b>File:</b> ${task.output || "N/A"}`;
        showPreview(task.output);
      } else {
        statusBox.innerHTML = `⏳ Task: ${taskId}<br>Status: ${task.status}<br>Notes: ${task.notes?.slice(-1)[0] || "Working..."}`;
      }
    } catch {
      clearInterval(interval);
      statusBox.innerHTML = "❌ Error checking task status.";
    }
  }, 5000);
}

// Preview render video
function showPreview(outputPath) {
  if (!outputPath) return;
  const video = document.createElement("video");
  video.src = outputPath;
  video.controls = true;
  video.style.width = "80%";
  video.style.marginTop = "10px";
  previewBox.innerHTML = "";
  previewBox.appendChild(video);
}

startBtn.addEventListener("click", createTask);
checkStatus();
setInterval(checkStatus, 20000); // every 20 sec auto refresh
