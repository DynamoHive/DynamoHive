import React from "react";
import Header from "./Header";

function App() {
  return (
    <div style={{ background: "#0B0B0F", minHeight: "100vh" }}>

      <Header />

      <div style={{
        color: "white",
        padding: "40px",
        textAlign: "center"
      }}>
        <h2>System Active</h2>
      </div>

    </div>
  );
}

export default App;
