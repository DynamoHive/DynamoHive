import React from "react";
import Header from "./Header";
import SignalCard from "./SignalCard";

function App() {
  return (
    <div style={{ background: "#0B0B0F", minHeight: "100vh" }}>

      <Header />

      <SignalCard />

      <div style={{
        color: "white",
        padding: "20px",
        textAlign: "center",
        opacity: 0.6
      }}>
        System Active
      </div>

    </div>
  );
}

export default App;
