import React, { useEffect, useState } from "react";
import Header from "./Header";

function App() {

  const [signal, setSignal] = useState(null);

  useEffect(() => {
    fetch("https://dynamohive-ktzh.onrender.com/feed")
      .then(res => res.json())
      .then(data => {
        if (data && data.length > 0) {
          setSignal(data[0]);
        }
      })
      .catch(err => console.log(err));
  }, []);

  return (
    <div style={{ background: "#0B0B0F", minHeight: "100vh" }}>

      <Header />

      {!signal ? (
        <div style={{ color: "white", textAlign: "center", marginTop: "60px" }}>
          Loading signal...
        </div>
      ) : (
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

          <h2 style={{ fontSize: "20px", marginBottom: "20px" }}>
            {signal.title || "No title"}
          </h2>

          <div style={{
            display: "flex",
            justifyContent: "space-between",
            fontSize: "14px",
            marginBottom: "20px"
          }}>
            <span>Priority: {signal.priority || "N/A"}</span>
            <span>Confidence: {signal.confidence || "N/A"}</span>
          </div>

          <p style={{
            fontSize: "14px",
            lineHeight: "1.6",
            opacity: 0.8
          }}>
            {signal.content || ""}
          </p>

        </div>
      )}

    </div>
  );
}

export default App;
