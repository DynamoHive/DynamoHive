import React, { useState } from "react";

function Navbar() {
  const [menuOpen, setMenuOpen] = useState(false);

  return (
    <nav className="w-full bg-[#0B0B0F] border-b border-[#1F2937] text-white">
      
      <div className="max-w-7xl mx-auto px-4 py-3 flex items-center justify-between">

        {/* LEFT - Brand */}
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-md bg-gradient-to-r from-[#00D1FF] to-[#0099CC]" />
          <span className="text-lg font-semibold tracking-wide">
            DynamoHive
          </span>
        </div>

        {/* CENTER - Links (desktop) */}
        <div className="hidden md:flex gap-8 text-sm text-gray-300">
          <a href="#dashboard" className="hover:text-[#00D1FF] transition">
            Dashboard
          </a>
          <a href="#signals" className="hover:text-[#00D1FF] transition">
            Signals
          </a>
          <a href="#analytics" className="hover:text-[#00D1FF] transition">
            Analytics
          </a>
          <a href="#intelligence" className="hover:text-[#00D1FF] transition">
            Intelligence
          </a>
        </div>

        {/* RIGHT - Status + CTA */}
        <div className="hidden md:flex items-center gap-4">
          
          {/* System status */}
          <div className="flex items-center gap-2 text-xs text-gray-400">
            <span className="w-2 h-2 rounded-full bg-green-400 animate-pulse"></span>
            LIVE SYSTEM
          </div>

          {/* CTA */}
          <button className="px-4 py-2 rounded-md bg-[#00D1FF] text-black font-medium hover:bg-[#0099CC] transition">
            Enter Hive
          </button>
        </div>

        {/* MOBILE BUTTON */}
        <button
          onClick={() => setMenuOpen(!menuOpen)}
          className="md:hidden text-gray-300"
        >
          ☰
        </button>
      </div>

      {/* MOBILE MENU */}
      {menuOpen && (
        <div className="md:hidden px-4 pb-4 flex flex-col gap-3 text-sm text-gray-300">
          <a href="#dashboard">Dashboard</a>
          <a href="#signals">Signals</a>
          <a href="#analytics">Analytics</a>
          <a href="#intelligence">Intelligence</a>

          <button className="mt-2 px-4 py-2 rounded-md bg-[#00D1FF] text-black font-medium">
            Enter Hive
          </button>
        </div>
      )}
    </nav>
  );
}

export default Navbar;
