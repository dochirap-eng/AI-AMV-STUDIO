import React, { useState } from "react";
import "./Upload.css";

export default function Upload() {
  const [file, setFile] = useState(null);
  const [progress, setProgress] = useState(0);
  const [status, setStatus] = useState("Idle");

  const handlePick = (e) => {
    const f = e.target.files[0];
    if (!f) return;
    setFile(f);
    setStatus("Selected: " + f.name);
  };

  const handleUpload = async () => {
    if (!file) return setStatus("Choose a file first");
    setStatus("Uploading...");
    setProgress(0);

    const form = new FormData();
    form.append("file", file);

    // xhr for progress (works in mobile browsers)
    const xhr = new XMLHttpRequest();
    xhr.open("POST", "http://localhost:5000/upload", true);

    xhr.upload.onprogress = (ev) => {
      if (ev.lengthComputable) {
        const p = Math.round((ev.loaded / ev.total) * 100);
        setProgress(p);
      }
    };

    xhr.onload = () => {
      if (xhr.status >= 200 && xhr.status < 300) {
        try {
          const res = JSON.parse(xhr.responseText);
          setStatus("✅ Uploaded: " + (res.filename || "ok"));
        } catch (e) {
          setStatus("Uploaded (no JSON)");
        }
        setProgress(100);
      } else {
        setStatus("Upload failed: " + xhr.statusText);
      }
    };

    xhr.onerror = () => setStatus("Network error");

    xhr.send(form);
  };

  return (
    <div className="upload-page">
      <h2>AI Upload Panel</h2>
      <div className="upload-box">
        <input id="fileInput" type="file" accept="audio/*,video/*" style={{ display: "none" }} onChange={handlePick} />
        <label className="btn" htmlFor="fileInput">Choose File</label>
        <div className="filename">{file ? file.name : "No file chosen"}</div>

        <button className="btn primary" onClick={handleUpload}>Upload</button>

        <div className="progress-wrap">
          <div className="progress" style={{ width: progress + "%" }}>{progress}%</div>
        </div>

        <div className="status">{status}</div>
      </div>
    </div>
  );
}
