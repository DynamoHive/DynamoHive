export default function SignalCard() {
  return (
    <div style={{
      maxWidth: "600px",
      margin: "60px auto",
      padding: "30px",
      background: "#111117",
      border: "1px solid #1f1f2a",
      borderRadius: "10px",
      color: "white"
    }}>

      <div style={{
        fontSize: "12px",
        color: "#888",
        marginBottom: "10px",
        letterSpacing: "1px"
      }}>
        DETECTED SIGNAL
      </div>

      <h2 style={{
        fontSize: "20px",
        marginBottom: "20px"
      }}>
        Global AI infrastructure shift detected
      </h2>

      <div style={{
        display: "flex",
        justifyContent: "space-between",
        fontSize: "14px",
        marginBottom: "20px"
      }}>
        <span>Priority: HIGH</span>
        <span>Confidence: 0.82</span>
      </div>

      <button style={{
        width: "100%",
        padding: "10px",
        background: "#00FFC6",
        border: "none",
        color: "#000",
        fontWeight: "600",
        cursor: "pointer"
      }}>
        View Analysis
      </button>

    </div>
  );
}
