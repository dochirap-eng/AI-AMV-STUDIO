// ===== AI AMV STUDIO — main.js =====

function startAnalysis() {
  const fileInput = document.getElementById("fileInput");
  const statusBox = document.getElementById("statusBox");
  const content = document.querySelector(".content");

  if (!fileInput.files.length) {
    statusBox.innerHTML = "<p>⚠️ Please select a song first.</p>";
    return;
  }

  // Show fake upload animation
  statusBox.innerHTML = `
    <p>🎧 Uploading your song...</p>
    <div class="progress-container">
      <div class="progress-bar"></div>
    </div>
  `;

  const progressBar = document.querySelector(".progress-bar");
  let progress = 0;

  // Fake upload progress (simulate 3 sec upload)
  const uploadInterval = setInterval(() => {
    progress += 5;
    if (progress <= 100) {
      progressBar.style.width = progress + "%";
    }

    if (progress >= 100) {
      clearInterval(uploadInterval);
      statusBox.innerHTML = "<p>✅ Song uploaded successfully!</p>";

      // Play analysis animation video on top
      playOverlayVideo("/assets/analysis_scene.mp4");

      // After 5 seconds, move to video generation stage
      setTimeout(() => {
        showVideoUploadStage();
      }, 5000);
    }
  }, 150);
}

// 🔹 Play temporary animation video over content
function playOverlayVideo(src) {
  // Remove existing overlay if any
  const oldVid = document.getElementById("overlayVid");
  if (oldVid) oldVid.remove();

  const video = document.createElement("video");
  video.id = "overlayVid";
  video.src = src;
  video.autoplay = true;
  video.muted = true;
  video.playsInline = true;
  video.style.position = "absolute";
  video.style.top = "50%";
  video.style.left = "50%";
  video.style.transform = "translate(-50%, -50%)";
  video.style.width = "80%";
  video.style.height = "auto";
  video.style.zIndex = "999";
  video.style.borderRadius = "20px";
  video.style.boxShadow = "0 0 30px #ff69b4";

  document.body.appendChild(video);

  // Remove after playback
  video.onended = () => {
    video.remove();
  };
}

// 🔹 After song upload → show clip upload or generate video options
function showVideoUploadStage() {
  const content = document.querySelector(".content");
  content.innerHTML = `
    <h1 class="title">🎬 Step 2: Video Setup</h1>
    <p class="subtitle">Choose your method to continue</p>

    <div class="upload-box">
      <label>🎞 Upload Your Video Clip</label>
      <input type="file" id="clipInput" />
      <button onclick="generateFinalVideo()">Generate Video</button>
    </div>

    <div class="status" id="statusBox"><p>Waiting for video...</p></div>
  `;
}

// 🔹 Fake render + show render animation
function generateFinalVideo() {
  const statusBox = document.getElementById("statusBox");
  const clipInput = document.getElementById("clipInput");

  if (!clipInput.files.length) {
    statusBox.innerHTML = "<p>⚠️ Please select a video clip first.</p>";
    return;
  }

  statusBox.innerHTML = `
    <p>⚡ Generating final AMV...</p>
    <div class="progress-container">
      <div class="progress-bar"></div>
    </div>
  `;

  const progressBar = document.querySelector(".progress-bar");
  let progress = 0;

  const renderInterval = setInterval(() => {
    progress += 4;
    if (progress <= 100) {
      progressBar.style.width = progress + "%";
    }

    if (progress >= 100) {
      clearInterval(renderInterval);
      statusBox.innerHTML = "<p>🎉 Video generated successfully!</p>";

      // Play final render animation video
      playOverlayVideo("/assets/render_scene.mp4");

      // After playback complete, show "done" screen
      setTimeout(() => {
        showFinalScreen();
      }, 6000);
    }
  }, 150);
}

// 🔹 Final screen after render
function showFinalScreen() {
  const content = document.querySelector(".content");
  content.innerHTML = `
    <h1 class="title">💫 AMV Ready 💫</h1>
    <p class="subtitle">Your Anime Music Video has been created successfully!</p>
    <button onclick="location.reload()">Create Another</button>
  `;
}
