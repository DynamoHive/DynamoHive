const theme = {

  // -------------------------
  // COLORS
  // -------------------------
  colors: {

    // Core
    background: "#0B0B0F",
    surface: "#12121A",
    surfaceAlt: "#181824",

    // Borders
    border: "#1F2937",

    // Brand
    primary: "#00D1FF",
    primaryDark: "#0099CC",
    primarySoft: "#163340",

    // Text
    text: "#EAEAEA",
    muted: "#9CA3AF",
    dim: "#6B7280",

    // Signal Severity
    low: "#22C55E",
    medium: "#F59E0B",
    high: "#EF4444",

    // Status
    success: "#10B981",
    warning: "#F59E0B",
    danger: "#DC2626",

    // Misc
    white: "#FFFFFF",
    black: "#000000"
  },


  // -------------------------
  // TYPOGRAPHY
  // -------------------------
  typography: {

    fontFamily: "Arial, sans-serif",

    hero: {
      fontSize: "72px",
      fontWeight: "700",
      lineHeight: "1.05"
    },

    h1: {
      fontSize: "48px",
      fontWeight: "700"
    },

    h2: {
      fontSize: "32px",
      fontWeight: "600"
    },

    h3: {
      fontSize: "24px",
      fontWeight: "600"
    },

    body: {
      fontSize: "16px",
      lineHeight: "1.7"
    },

    small: {
      fontSize: "14px",
      lineHeight: "1.5"
    }
  },


  // -------------------------
  // BORDER RADIUS
  // -------------------------
  radius: {

    card: "18px",

    button: "10px",

    pill: "999px"
  },


  // -------------------------
  // SPACING
  // -------------------------
  spacing: {

    xs: "6px",

    sm: "12px",

    md: "20px",

    lg: "40px",

    xl: "80px",

    section: "100px",

    container: "1100px"
  },


  // -------------------------
  // SHADOWS
  // -------------------------
  shadows: {

    card: "0 0 20px rgba(0,209,255,0.05)",

    glow: "0 0 30px rgba(0,209,255,0.15)"
  },


  // -------------------------
  // TRANSITIONS
  // -------------------------
  transitions: {

    default: "all 0.2s ease",

    slow: "all 0.4s ease"
  },


  // -------------------------
  // COMPONENT PRESETS
  // -------------------------
  components: {

    card: {
      background: "#12121A",
      border: "1px solid #1F2937",
      borderRadius: "18px",
      padding: "24px"
    },

    buttonPrimary: {
      background: "#00D1FF",
      color: "#000000",
      border: "none",
      borderRadius: "10px",
      padding: "14px 28px",
      cursor: "pointer",
      fontWeight: "600"
    },

    buttonSecondary: {
      background: "transparent",
      color: "#00D1FF",
      border: "1px solid #00D1FF",
      borderRadius: "10px",
      padding: "14px 28px",
      cursor: "pointer"
    }
  }
};


export default theme;
