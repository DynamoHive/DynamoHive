import React, { useState } from "react";

function Navbar() {

  const [menuOpen, setMenuOpen] = useState(false);

  return (

    <nav
      className="
        sticky
        top-0
        z-50
        w-full
        border-b
        border-[#1F2937]
        bg-[#0B0B0F]/90
        backdrop-blur-xl
        text-white
      "
    >

      <div
        className="
          max-w-7xl
          mx-auto
          px-6
          py-4
          flex
          items-center
          justify-between
        "
      >

        {/* ===================================================== */}
        {/* LEFT */}
        {/* ===================================================== */}

        <div className="flex items-center gap-4">

          {/* LOGO */}
          <div
            className="
              relative
              w-10
              h-10
              rounded-xl
              bg-gradient-to-br
              from-[#00D1FF]
              via-[#0099CC]
              to-[#0044FF]
              shadow-[0_0_25px_rgba(0,209,255,0.35)]
            "
          >

            <div
              className="
                absolute
                inset-1
                rounded-lg
                border
                border-white/10
              "
            />

          </div>

          {/* BRAND */}
          <div>

            <div
              className="
                text-xl
                font-bold
                tracking-wide
              "
            >
              DynamoHive
            </div>

            <div
              className="
                text-[11px]
                uppercase
                tracking-[0.25em]
                text-[#6B7280]
              "
            >
              Autonomous Intelligence
            </div>

          </div>

        </div>

        {/* ===================================================== */}
        {/* CENTER LINKS */}
        {/* ===================================================== */}

        <div
          className="
            hidden
            md:flex
            items-center
            gap-10
            text-sm
            text-gray-300
          "
        >

          <a
            href="#dashboard"
            className="
              hover:text-[#00D1FF]
              transition
            "
          >
            Dashboard
          </a>

          <a
            href="#signals"
            className="
              hover:text-[#00D1FF]
              transition
            "
          >
            Signals
          </a>

          <a
            href="#analytics"
            className="
              hover:text-[#00D1FF]
              transition
            "
          >
            Analytics
          </a>

          <a
            href="#intelligence"
            className="
              hover:text-[#00D1FF]
              transition
            "
          >
            Intelligence
          </a>

          <a
            href="/legal.html"
            className="
              hover:text-[#00D1FF]
              transition
            "
          >
            Legal
          </a>

          <a
            href="/privacy.html"
            className="
              hover:text-[#00D1FF]
              transition
            "
          >
            Privacy
          </a>

        </div>

        {/* ===================================================== */}
        {/* RIGHT */}
        {/* ===================================================== */}

        <div
          className="
            hidden
            md:flex
            items-center
            gap-5
          "
        >

          {/* LIVE STATUS */}
          <div
            className="
              flex
              items-center
              gap-2
              px-3
              py-2
              rounded-full
              border
              border-[#1F2937]
              bg-[#111827]
            "
          >

            <span
              className="
                w-2
                h-2
                rounded-full
                bg-green-400
                animate-pulse
              "
            />

            <span
              className="
                text-xs
                text-gray-300
                tracking-wide
              "
            >
              LIVE SYSTEM
            </span>

          </div>

          {/* CTA */}
          <button
            className="
              px-5
              py-2.5
              rounded-xl
              bg-[#00D1FF]
              text-black
              font-semibold
              hover:bg-[#00B8E6]
              transition
              shadow-[0_0_20px_rgba(0,209,255,0.35)]
            "
          >
            Enter Hive
          </button>

        </div>

        {/* ===================================================== */}
        {/* MOBILE BUTTON */}
        {/* ===================================================== */}

        <button
          onClick={() => setMenuOpen(!menuOpen)}
          className="
            md:hidden
            text-2xl
            text-gray-300
          "
        >
          ☰
        </button>

      </div>

      {/* ===================================================== */}
      {/* MOBILE MENU */}
      {/* ===================================================== */}

      {menuOpen && (

        <div
          className="
            md:hidden
            px-6
            pb-6
            flex
            flex-col
            gap-4
            text-sm
            text-gray-300
            border-t
            border-[#1F2937]
            bg-[#0B0B0F]
          "
        >

          <a href="#dashboard">
            Dashboard
          </a>

          <a href="#signals">
            Signals
          </a>

          <a href="#analytics">
            Analytics
          </a>

          <a href="#intelligence">
            Intelligence
          </a>

          <a href="/legal.html">
            Legal
          </a>

          <a href="/privacy.html">
            Privacy
          </a>

          <button
            className="
              mt-3
              px-4
              py-3
              rounded-xl
              bg-[#00D1FF]
              text-black
              font-semibold
            "
          >
            Enter Hive
          </button>

        </div>

      )}

    </nav>
  );
}

export default Navbar;
