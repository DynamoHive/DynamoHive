import React, { useEffect, useState } from "react";
import Header from "./Header";

function App() {

  const [signals, setSignals] = useState([]);
  const [system, setSystem] = useState({});

  useEffect(() => {

    const fetchData = async () => {
      try {

        const res = await fetch("https://dynamohive-ktzh.onrender.com/intel");
        const data = await res.json();

        // system info
        setSystem({
          status: data.status,
          cycle: data.cycle,
          last_update: data.last_update,
          items: data.items
        });

        // signals list (delta merge)
        setSignals(prev => {

          const existing = new Set(prev.map(i => i.id || i.title));

          const incoming = (data.data || []).filter(i => {
            return !existing.has(i.id || i.title);
          });

          return [...incoming, ...prev].slice(0, 100);
        });

      } catch (err) {
        console.log("fetch error:", err);
      }
    };

    fetchData();
    const interval = setInterval(fetchData, 3000);

    return () => clearInterval(interval);

  }, []);

  return (
    <div style={{ background: "#0B0B0F", minHeight: "100vh", color: "white" }}>

      <Header />

      {/* SYSTEM BAR */}
      <div style={{
        maxWidth: "900px",
        margin: "20px auto",
        fontSize: "12px",
        opacity: 0.7,
        display: "flex",
        justifyContent: "space-between"
      }}>
        <span>Status: {system.status}</span>
        <span>Cycle: {system.cycle}</span>
        <span>Items: {system.items}</span>
      </div>

      {/* FEED */}
      <div style={{
        maxWidth: "900px",
        margin: "40px auto",
        display: "flex",
        flexDirection: "column",
        gap: "12px"
      }}>

        {signals.length === 0 ? (
          <div style={{ textAlign: "center", opacity: 0.6 }}>
            Waiting for intelligence stream...
          </div>
        ) : (
          signals.map((signal, idx) => (
            <div key={signal.id || idx} style={{
              padding: "16px",
              background: "#111117",
              border: "1px solid #1f1f2a",
              borderRadius: "8px"
            }}>

              <div style={{ fontSize: "11px", opacity: 0.6 }}>
                SIGNAL #{idx + 1}
              </div>

              <h3 style={{ margin: "8px 0" }}>
                {signal.title}
              </h3>

              <div style={{
                display: "flex",
                justifyContent: "space-between",
                fontSize: "12px",
                opacity: 0.7,
                marginBottom: "8px"
              }}>
                <span>Priority: {signal.priority || "N/A"}</span>
                <span>Urgency: {signal.urgency || "N/A"}</span>
              </div>

              <p style={{ fontSize: "13px", opacity: 0.8 }}>
                {signal.content}
              </p>

            </div>
          ))
        )}

      </div>

    </div>
  );
}

export default App;
