const theme = {

  // -------------------------
  // COLORS
  // -------------------------
  colors: {

    // Core Backgrounds
    background: "#050505",
    surface: "#0F0F10",
    surfaceAlt: "#171717",

    // Borders
    border: "#242424",
    borderSoft: "#303030",

    // Brand (Gold Identity)
    primary: "#D4AF37",
    primarySoft: "#F1D27A",
    primaryDark: "#A67C1B",

    // Typography
    text: "#F5F5F5",
    muted: "#A1A1AA",
    dim: "#6B7280",

    // Signal Severity
    low: "#4ADE80",
    medium: "#FBBF24",
    high: "#F87171",

    // Status
    success: "#22C55E",
    warning: "#F59E0B",
    danger: "#EF4444",

    // Utility
    white: "#FFFFFF",
    black: "#000000"
  },


  // -------------------------
  // TYPOGRAPHY
  // -------------------------
  typography: {

    fontFamily: "'Inter', Arial, sans-serif",

    hero: {
      fontSize: "72px",
      fontWeight: "700",
      lineHeight: "1.05",
      letterSpacing: "-2px"
    },

    h1: {
      fontSize: "52px",
      fontWeight: "700",
      lineHeight: "1.1"
    },

    h2: {
      fontSize: "34px",
      fontWeight: "600",
      lineHeight: "1.2"
    },

    h3: {
      fontSize: "24px",
      fontWeight: "600",
      lineHeight: "1.3"
    },

    body: {
      fontSize: "16px",
      lineHeight: "1.8"
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

    card: "20px",

    button: "12px",

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

    section: "120px",

    container: "1200px"
  },


  // -------------------------
  // SHADOWS
  // -------------------------
  shadows: {

    card: "0 10px 30px rgba(0,0,0,0.35)",

    glow: "0 0 30px rgba(212,175,55,0.18)",

    soft: "0 4px 12px rgba(0,0,0,0.2)"
  },


  // -------------------------
  // TRANSITIONS
  // -------------------------
  transitions: {

    default: "all 0.25s ease",

    slow: "all 0.45s ease"
  },


  // -------------------------
  // COMPONENT PRESETS
  // -------------------------
  components: {

    card: {
      background: "#0F0F10",
      border: "1px solid #242424",
      borderRadius: "20px",
      padding: "28px",
      boxShadow: "0 10px 30px rgba(0,0,0,0.35)"
    },

    buttonPrimary: {
      background: "#D4AF37",
      color: "#000000",
      border: "none",
      borderRadius: "12px",
      padding: "14px 30px",
      cursor: "pointer",
      fontWeight: "700",
      transition: "all 0.25s ease"
    },

    buttonSecondary: {
      background: "transparent",
      color: "#D4AF37",
      border: "1px solid #D4AF37",
      borderRadius: "12px",
      padding: "14px 30px",
      cursor: "pointer",
      fontWeight: "600",
      transition: "all 0.25s ease"
    },

    navbar: {
      background: "rgba(5,5,5,0.9)",
      borderBottom: "1px solid #242424",
      backdropFilter: "blur(12px)"
    }
  }
};


export default theme;
