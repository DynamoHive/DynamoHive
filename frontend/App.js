import React, { useEffect, useState } from "react";
import Landing from "./Landing";

function Dashboard() {

  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  const fetchData = () => {
    fetch("https://dynamohive-ktzh.onrender.com/intel")
      .then(res => res.json())
      .then(res => {
        setData(res);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  };

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 15000);
    return () => clearInterval(interval);
  }, []);

  const signals = data?.data || [];

  const getColor = (p) => {
    if (p >= 0.7) return "#ff4d4d";
    if (p >= 0.4) return "#ffa500";
    return "#4da6ff";
  };

  return (
    <div style={{ background: "#0B0B0F", minHeight: "100vh", color: "white" }}>

      <div style={{
        maxWidth: "900px",
        margin: "0 auto",
        padding: "20px",
        display: "flex",
        justifyContent: "space-between",
        fontSize: "13px",
        opacity: 0.7
      }}>
        <span>Cycle: {data?.cycle || "-"}</span>
        <span>Signals: {signals.length}</span>
        <span>
          Updated: {data?.last_update
            ? new Date(data.last_update * 1000).toLocaleTimeString()
            : "-"}
        </span>
      </div>

      {loading ? (
        <div style={{ textAlign: "center", marginTop: 100 }}>
          Loading intelligence feed...
        </div>
      ) : signals.length === 0 ? (
        <div style={{ textAlign: "center", marginTop: 100, opacity: 0.6 }}>
          No signals detected
        </div>
      ) : (
        signals
          .sort((a, b) => (b.priority || 0) - (a.priority || 0))
          .map((s, i) => (
            <div key={i} style={{
              maxWidth: 800,
              margin: "15px auto",
              padding: 20,
              background: "#111117",
              borderRadius: 10,
              border: "1px solid #1f1f2a",
              borderLeft: `4px solid ${getColor(s.priority || 0)}`
            }}>

              <div style={{ fontSize: 16, fontWeight: "bold" }}>
                {s.title}
              </div>

              <div style={{
                fontSize: 12,
                opacity: 0.6,
                marginTop: 8,
                display: "flex",
                justifyContent: "space-between"
              }}>
                <span>Priority: {s.priority?.toFixed(2) || "0.00"}</span>
                <span>{s.published ? "LIVE" : "DRAFT"}</span>
              </div>

              <div style={{
                marginTop: 12,
                fontSize: 14,
                lineHeight: 1.6,
                opacity: 0.85
              }}>
                {s.content}
              </div>

            </div>
          ))
      )}

    </div>
  );
}

export default function App() {
  return <Dashboard />;
}
