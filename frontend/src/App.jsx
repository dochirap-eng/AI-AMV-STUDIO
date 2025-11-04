import React, { useState } from "react";
import "./App.css";

function App() {
  const [activePage, setActivePage] = useState("dashboard");

  return (
    <div className="app-container">
      {/* Sidebar */}
      <aside className="sidebar">
        <h2 className="logo">AI AMV STUDIO</h2>
        <nav>
          <ul>
            <li
              className={activePage === "dashboard" ? "active" : ""}
              onClick={() => setActivePage("dashboard")}
            >
              Dashboard
            </li>
            <li
              className={activePage === "projects" ? "active" : ""}
              onClick={() => setActivePage("projects")}
            >
              Projects
            </li>
            <li
              className={activePage === "settings" ? "active" : ""}
              onClick={() => setActivePage("settings")}
            >
              Settings
            </li>
          </ul>
        </nav>
      </aside>

      {/* Main Content */}
      <main className="content fade-in">
        {activePage === "dashboard" && (
          <section className="dashboard">
            <h1>Dashboard</h1>
            <div className="card-grid">
              <div className="card glow">🎵 Auto Beat Sync</div>
              <div className="card glow">🎬 Clip Analyzer</div>
              <div className="card glow">⚙️ Render Optimizer</div>
              <div className="card glow">💡 Smart Scene Match</div>
            </div>
          </section>
        )}

        {activePage === "projects" && (
          <section className="projects fade-in">
            <h1>My Projects</h1>
            <p>Coming soon: Manage and preview your AMVs here.</p>
          </section>
        )}

        {activePage === "settings" && (
          <section className="settings fade-in">
            <h1>Settings</h1>
            <p>Adjust theme, model preferences, and export options.</p>
          </section>
        )}
      </main>
    </div>
  );
}

export default App;
