export default function Header() {
  return (
    <div style={{
      position: "relative",
      height: "80px",
      background: "#0B0B0F",
      borderBottom: "1px solid #1a1a1a"
    }}>

      <img
        src="/logo.png"
        style={{
          position: "absolute",
          left: "20px",
          top: "50%",
          transform: "translateY(-50%)",
          height: "32px"
        }}
      />

      <div style={{
        position: "absolute",
        left: "50%",
        top: "50%",
        transform: "translate(-50%, -50%)",
        color: "white",
        fontSize: "20px",
        fontWeight: "600"
      }}>
        DynamoHive
      </div>

    </div>
  );
}
