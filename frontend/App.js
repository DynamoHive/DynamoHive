import React, { useEffect, useState } from "react";

import Navbar from "./components/Navbar";
import Landing from "./Landing";


function Dashboard() {

  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  // =====================================================
  // FETCH
  // =====================================================

  const fetchData = () => {

    fetch("https://dynamohive-ktzh.onrender.com/intel")

      .then(res => res.json())

      .then(res => {

        setData(res);
        setLoading(false);

      })

      .catch(() => {

        setLoading(false);

      });

  };

  // =====================================================
  // LIVE REFRESH
  // =====================================================

  useEffect(() => {

    fetchData();

    const interval = setInterval(fetchData, 15000);

    return () => clearInterval(interval);

  }, []);

  const signals = data?.data || [];

  // =====================================================
  // PRIORITY COLOR
  // =====================================================

  const getColor = (p) => {

    if (p >= 0.7) return "#ff4d4d";
    if (p >= 0.4) return "#ffa500";

    return "#00D1FF";

  };

  // =====================================================
  // UI
  // =====================================================

  return (

    <div
      style={{
        background: "#0B0B0F",
        minHeight: "100vh",
        color: "white",
        fontFamily: "Inter, sans-serif"
      }}
    >

      {/* ================================================= */}
      {/* NAVBAR */}
      {/* ================================================= */}

      <Navbar />

      {/* ================================================= */}
      {/* LANDING */}
      {/* ================================================= */}

      <Landing />

      {/* ================================================= */}
      {/* DASHBOARD HEADER */}
      {/* ================================================= */}

      <div
        id="dashboard"
        style={{
          maxWidth: "1200px",
          margin: "0 auto",
          padding: "60px 24px 20px"
        }}
      >

        <div
          style={{
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
            flexWrap: "wrap",
            gap: "20px",
            marginBottom: "40px"
          }}
        >

          <div>

            <div
              style={{
                color: "#00D1FF",
                fontSize: "14px",
                letterSpacing: "0.2em",
                textTransform: "uppercase",
                marginBottom: "10px"
              }}
            >
              Live Intelligence Feed
            </div>

            <h1
              style={{
                fontSize: "42px",
                margin: 0,
                fontWeight: "800"
              }}
            >
              Global Signal Monitoring
            </h1>

          </div>

          {/* STATUS PANEL */}

          <div
            style={{
              display: "flex",
              gap: "16px",
              flexWrap: "wrap"
            }}
          >

            <StatusCard
              label="Cycle"
              value={data?.cycle || "-"}
            />

            <StatusCard
              label="Signals"
              value={signals.length}
            />

            <StatusCard
              label="Updated"
              value={
                data?.last_update
                  ? new Date(
                      data.last_update * 1000
                    ).toLocaleTimeString()
                  : "-"
              }
            />

          </div>

        </div>

      </div>

      {/* ================================================= */}
      {/* LOADING */}
      {/* ================================================= */}

      {loading ? (

        <div
          style={{
            textAlign: "center",
            padding: "120px 20px",
            color: "#9CA3AF"
          }}
        >
          Loading intelligence feed...
        </div>

      ) : signals.length === 0 ? (

        <div
          style={{
            textAlign: "center",
            padding: "120px 20px",
            color: "#6B7280"
          }}
        >
          No active signals detected
        </div>

      ) : (

        <div
          id="signals"
          style={{
            maxWidth: "1200px",
            margin: "0 auto",
            padding: "0 24px 80px"
          }}
        >

          {signals

            .sort(
              (a, b) =>
                (b.priority || 0) -
                (a.priority || 0)
            )

            .map((s, i) => (

              <div
                key={i}
                style={{
                  background: "#111117",
                  border: "1px solid #1F2937",
                  borderLeft: `5px solid ${getColor(
                    s.priority || 0
                  )}`,
                  borderRadius: "18px",
                  padding: "28px",
                  marginBottom: "22px",
                  boxShadow:
                    "0 0 25px rgba(0,0,0,0.25)"
                }}
              >

                {/* TITLE */}

                <div
                  style={{
                    fontSize: "22px",
                    fontWeight: "700",
                    marginBottom: "14px",
                    lineHeight: 1.3
                  }}
                >
                  {s.title}
                </div>

                {/* META */}

                <div
                  style={{
                    display: "flex",
                    justifyContent: "space-between",
                    flexWrap: "wrap",
                    gap: "10px",
                    fontSize: "13px",
                    color: "#9CA3AF",
                    marginBottom: "20px"
                  }}
                >

                  <span>
                    Priority:
                    {" "}
                    {s.priority?.toFixed(2) || "0.00"}
                  </span>

                  <span>
                    Status:
                    {" "}
                    {s.published
                      ? "LIVE"
                      : "DRAFT"}
                  </span>

                </div>

                {/* CONTENT */}

                <div
                  style={{
                    lineHeight: 1.8,
                    color: "#D1D5DB",
                    fontSize: "15px"
                  }}
                >
                  {s.content}
                </div>

              </div>

            ))}

        </div>

      )}

    </div>

  );

}


// =====================================================
// STATUS CARD
// =====================================================

function StatusCard({ label, value }) {

  return (

    <div
      style={{
        background: "#111827",
        border: "1px solid #1F2937",
        borderRadius: "16px",
        padding: "18px 22px",
        minWidth: "130px"
      }}
    >

      <div
        style={{
          color: "#6B7280",
          fontSize: "12px",
          marginBottom: "8px",
          textTransform: "uppercase",
          letterSpacing: "0.08em"
        }}
      >
        {label}
      </div>

      <div
        style={{
          color: "#00D1FF",
          fontWeight: "700",
          fontSize: "20px"
        }}
      >
        {value}
      </div>

    </div>

  );

}


// =====================================================
// APP
// =====================================================

export default function App() {

  return <Dashboard />;

}
