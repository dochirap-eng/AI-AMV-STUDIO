import React, { useState } from "react";
import "./Projects.css";

export default function Projects() {
  const [song, setSong] = useState(null);
  const [status, setStatus] = useState("Idle");

  const handleSongUpload = async (e) => {
    const file = e.target.files[0];
    setSong(file);
    setStatus("🎵 Uploading song to AI backend...");

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch("http://localhost:5000/analyze", {
        method: "POST",
        body: formData,
      });
      const result = await response.json();
      setStatus(`✅ ${result.message}`);
    } catch (err) {
      console.error(err);
      setStatus("❌ Error sending file to backend!");
    }
  };

  return (
    <div className="projects-page">
      <h2>AI Creation Panel</h2>
      <div className="upload-section">
        <label className="upload-btn">
          Upload Song (MP3)
          <input type="file" accept="audio/*" onChange={handleSongUpload} hidden />
        </label>
      </div>
      <p className="status-text">{status}</p>
    </div>
  );
}
