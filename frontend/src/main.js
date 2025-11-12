const audioInput = document.getElementById("audioFile");
const videoInput = document.getElementById("videoFiles");
const promptInput = document.getElementById("promptInput");
const startBtn = document.getElementById("startBtn");
const statusBox = document.getElementById("statusBox");
const previewBox = document.getElementById("previewBox");

startBtn.onclick = async () => {
  statusBox.innerHTML = "⏳ Uploading...";

  const form = new FormData();
  if (audioInput.files[0]) form.append("audio", audioInput.files[0]);
  for (let f of videoInput.files) form.append("video", f);
  form.append("prompt", promptInput.value);

  const res = await fetch("http://localhost:5000/api/tasks/new", {
    method: "POST",
    body: form
  });

  const data = await res.json();

  if (!data.ok) {
    statusBox.innerHTML = "❌ Failed to create task";
    return;
  }

  statusBox.innerHTML = `✅ Task Created: <b>${data.taskId}</b>`;

  previewBox.innerHTML = `
    <p>Task ID: ${data.taskId}</p>
    <button onclick="checkTask('${data.taskId}')">Check Status</button>
  `;
};

window.checkTask = async (id) => {
  const res = await fetch(`http://localhost:5000/api/tasks/${id}`);
  const data = await res.json();
  statusBox.innerHTML = `<pre>${JSON.stringify(data, null, 2)}</pre>`;
};
