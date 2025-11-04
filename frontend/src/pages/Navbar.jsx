import React from "react";

const Navbar = () => {
  return (
    <nav className="flex items-center justify-between px-8 py-4 bg-gradient-to-r from-[#0f0f0f]/90 to-[#1a1a1a]/90 backdrop-blur-lg border-b border-white/10 shadow-lg sticky top-0 z-50">
      <h1 className="text-2xl font-bold text-white tracking-wide hover:scale-105 transition-transform duration-300">
        ⚡ AI AMV STUDIO
      </h1>

      <div className="flex items-center gap-6">
        <a
          href="#"
          className="text-gray-300 hover:text-white text-sm font-medium transition-all duration-200"
        >
          Dashboard
        </a>
        <a
          href="#"
          className="text-gray-300 hover:text-white text-sm font-medium transition-all duration-200"
        >
          Projects
        </a>
        <a
          href="#"
          className="text-gray-300 hover:text-white text-sm font-medium transition-all duration-200"
        >
          Settings
        </a>
        <button className="px-4 py-2 rounded-xl bg-gradient-to-r from-purple-500 to-blue-600 text-white font-semibold shadow-md hover:shadow-xl hover:scale-105 transition-all duration-300">
          + New Project
        </button>
      </div>
    </nav>
  );
};

export default Navbar;
