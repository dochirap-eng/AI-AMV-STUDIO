import React from "react";
import "./Dashboard.css";

const Dashboard = () => {
  const cards = [
    { title: "🎬 Create New AMV", desc: "Auto-edit from clips & music" },
    { title: "🎵 Audio Sync", desc: "AI detects beats & matches scenes" },
    { title: "⚡ Quick Render", desc: "Fast preview & export in HD" },
    { title: "🧠 Smart Analysis", desc: "Scene + emotion recognition" },
  ];

  return (
    <div className="dashboard">
      <h1 className="dashboard-title">AI AMV STUDIO DASHBOARD</h1>
      <div className="card-grid">
        {cards.map((card, index) => (
          <div key={index} className="dash-card">
            <h3>{card.title}</h3>
            <p>{card.desc}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Dashboard;
