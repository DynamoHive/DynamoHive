import React, { useEffect, useState } from "react";
import Landing from "./Landing";

function Dashboard() {

  const [signal, setSignal] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {

    fetch("https://dynamohive-ktzh.onrender.com/intel")
      .then(res => res.json())
      .then(data => {

        const list = data?.data || [];

        if (list.length > 0) {
          setSignal(list[0]);
        }

        setLoading(false);

      })
      .catch(err => {
        console.log(err);
        setLoading(false);
      });

  }, []);

  return (

    <div style={{ background: "#0B0B0F", minHeight: "100vh" }}>

      {loading ? (

        <div style={{
          color: "white",
          textAlign: "center",
          paddingTop: "100px"
        }}>
          Loading intelligence...
        </div>

      ) : !signal ? (

        <div style={{
          color: "white",
          textAlign: "center",
          paddingTop: "100px",
          opacity: 0.6
        }}>
          No signals detected
        </div>

      ) : (

        <div style={{
          maxWidth: "700px",
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
            fontSize: "24px",
            marginBottom: "20px"
          }}>
            {signal.title || "No title"}
          </h2>

          <div style={{
            display: "flex",
            justifyContent: "space-between",
            fontSize: "14px",
            marginBottom: "20px",
            color: "#999"
          }}>
            <span>
              Priority: {signal.priority ?? "N/A"}
            </span>

            <span>
              Published: {signal.published ? "YES" : "NO"}
            </span>
          </div>

          <p style={{
            fontSize: "15px",
            lineHeight: "1.7",
            opacity: 0.85
          }}>
            {signal.content || ""}
          </p>

        </div>

      )}

    </div>

  );
}

export default function App() {

  const path = window.location.pathname;

  if (path === "/dashboard") {
    return <Dashboard />;
  }

  return <Landing />;
}
