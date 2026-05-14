import React, { useEffect, useState } from "react";
import Landing from "./Landing";

function Dashboard() {

  const [signal, setSignal] = useState(null);

  useEffect(() => {

    fetch("https://dynamohive-ktzh.onrender.com/intel")
      .then(res => res.json())
      .then(data => {

        if (data && data.data && data.data.length > 0) {

          setSignal(data.data[0]);

        }

      })
      .catch(err => console.log(err));

  }, []);

  return (

    <div style={{ background: "#0B0B0F", minHeight: "100vh" }}>

      {!signal ? (

        <div
          style={{
            color: "white",
            textAlign: "center",
            paddingTop: "100px"
          }}
        >
          Loading intelligence...
        </div>

      ) : (

        <div
          style={{
            maxWidth: "700px",
            margin: "60px auto",
            padding: "30px",
            background: "#111117",
            border: "1px solid #1f1f2a",
            borderRadius: "10px",
            color: "white"
          }}
        >

          <div
            style={{
              fontSize: "12px",
              color: "#888",
              marginBottom: "10px",
              letterSpacing: "1px"
            }}
          >
            DETECTED SIGNAL
          </div>

          <h2
            style={{
              fontSize: "24px",
              marginBottom: "20px"
            }}
          >
            {signal.title || "No title"}
          </h2>

          <div
            style={{
              display: "flex",
              justifyContent: "space-between",
              fontSize: "14px",
              marginBottom: "20px",
              color: "#999"
            }}
          >
            <span>
              Priority: {signal.priority || "N/A"}
            </span>

            <span>
              Published: {signal.published ? "YES" : "NO"}
            </span>
          </div>

          <p
            style={{
              fontSize: "15px",
              lineHeight: "1.7",
              opacity: 0.85
            }}
          >
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
