import React from "react";
import Navbar from "./components/Navbar";

function Landing() {

  return (

    <div
      style={{
        background: "#0B0B0F",
        minHeight: "100vh",
        color: "#FFFFFF",
        fontFamily: "Inter, sans-serif"
      }}
    >

      <Navbar />

      {/* HERO */}
      <section
        style={{
          padding: "120px 30px 100px",
          borderBottom: "1px solid #1F2937"
        }}
      >

        <div
          style={{
            maxWidth: "1400px",
            margin: "0 auto",
            display: "grid",
            gridTemplateColumns: "repeat(auto-fit,minmax(320px,1fr))",
            gap: "60px",
            alignItems: "center"
          }}
        >

          {/* LEFT */}
          <div>

            <div
              style={{
                display: "inline-flex",
                alignItems: "center",
                gap: "10px",
                background: "#111827",
                border: "1px solid #1F2937",
                padding: "10px 18px",
                borderRadius: "999px",
                marginBottom: "28px",
                color: "#00D1FF",
                fontSize: "14px",
                fontWeight: "600"
              }}
            >
              <span
                style={{
                  width: "10px",
                  height: "10px",
                  borderRadius: "50%",
                  background: "#00FF94",
                  boxShadow: "0 0 12px #00FF94"
                }}
              />
              LIVE AUTONOMOUS SYSTEM
            </div>

            <h1
              style={{
                fontSize: "72px",
                lineHeight: "1.05",
                marginBottom: "28px",
                fontWeight: "800",
                letterSpacing: "-2px"
              }}
            >
              Autonomous
              <br />
              Intelligence
              <br />
              Infrastructure
            </h1>

            <p
              style={{
                color: "#9CA3AF",
                fontSize: "20px",
                lineHeight: "1.8",
                maxWidth: "700px",
                marginBottom: "40px"
              }}
            >
              DynamoHive monitors geopolitical instability,
              AI acceleration, information warfare,
              economic disruption and global crisis signals
              through autonomous multi-layer intelligence pipelines.
            </p>

            <div
              style={{
                display: "flex",
                gap: "20px",
                flexWrap: "wrap"
              }}
            >

              <button
                style={{
                  background: "#00D1FF",
                  color: "#000",
                  border: "none",
                  padding: "16px 28px",
                  borderRadius: "14px",
                  fontWeight: "700",
                  fontSize: "16px",
                  cursor: "pointer"
                }}
              >
                Enter Intelligence Layer
              </button>

              <button
                style={{
                  background: "transparent",
                  color: "#FFFFFF",
                  border: "1px solid #1F2937",
                  padding: "16px 28px",
                  borderRadius: "14px",
                  fontWeight: "600",
                  fontSize: "16px",
                  cursor: "pointer"
                }}
              >
                View Live Signals
              </button>

            </div>

          </div>

          {/* RIGHT */}
          <div>

            <div
              style={{
                background: "#12121A",
                border: "1px solid #1F2937",
                borderRadius: "24px",
                padding: "30px"
              }}
            >

              <div
                style={{
                  display: "flex",
                  justifyContent: "space-between",
                  marginBottom: "30px"
                }}
              >

                <div>
                  <div
                    style={{
                      color: "#6B7280",
                      marginBottom: "10px",
                      fontSize: "14px"
                    }}
                  >
                    SYSTEM STATUS
                  </div>

                  <div
                    style={{
                      color: "#00FF94",
                      fontWeight: "700",
                      fontSize: "24px"
                    }}
                  >
                    ACTIVE
                  </div>
                </div>

                <div>
                  <div
                    style={{
                      color: "#6B7280",
                      marginBottom: "10px",
                      fontSize: "14px"
                    }}
                  >
                    SIGNAL FLOW
                  </div>

                  <div
                    style={{
                      color: "#00D1FF",
                      fontWeight: "700",
                      fontSize: "24px"
                    }}
                  >
                    REAL-TIME
                  </div>
                </div>

              </div>

              <div
                style={{
                  display: "grid",
                  gridTemplateColumns: "repeat(2,1fr)",
                  gap: "18px"
                }}
              >

                <StatusCard
                  title="AI Signals"
                  value="1,284"
                />

                <StatusCard
                  title="Geopolitical"
                  value="342"
                />

                <StatusCard
                  title="Threat Events"
                  value="89"
                />

                <StatusCard
                  title="Sources"
                  value="71"
                />

              </div>

            </div>

          </div>

        </div>

      </section>

      {/* FEATURES */}
      <section
        style={{
          padding: "100px 30px"
        }}
      >

        <div
          style={{
            maxWidth: "1400px",
            margin: "0 auto"
          }}
        >

          <div
            style={{
              marginBottom: "60px"
            }}
          >

            <h2
              style={{
                fontSize: "48px",
                marginBottom: "20px"
              }}
            >
              Intelligence Architecture
            </h2>

            <p
              style={{
                color: "#9CA3AF",
                fontSize: "18px",
                maxWidth: "800px",
                lineHeight: "1.8"
              }}
            >
              DynamoHive combines autonomous crawling,
              signal clustering, narrative analysis,
              crisis detection and strategic forecasting
              into a unified intelligence infrastructure.
            </p>

          </div>

          <div
            style={{
              display: "grid",
              gridTemplateColumns: "repeat(auto-fit,minmax(280px,1fr))",
              gap: "24px"
            }}
          >

            <FeatureCard
              title="Signal Detection"
              text="Detects emerging geopolitical, technological and economic anomalies in real time."
            />

            <FeatureCard
              title="Narrative Analysis"
              text="Tracks information warfare patterns and media influence structures."
            />

            <FeatureCard
              title="Crisis Radar"
              text="Identifies high-risk instability events and escalation patterns."
            />

            <FeatureCard
              title="Strategic Forecasting"
              text="Generates intelligence predictions from autonomous reasoning pipelines."
            />

          </div>

        </div>

      </section>

      {/* FOOTER */}
      <footer
        style={{
          marginTop: "80px",
          padding: "40px 30px",
          borderTop: "1px solid #1F2937"
        }}
      >

        <div
          style={{
            maxWidth: "1400px",
            margin: "0 auto",
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
            flexWrap: "wrap",
            gap: "20px"
          }}
        >

          <div
            style={{
              color: "#6B7280",
              fontSize: "14px"
            }}
          >
            © 2026 DynamoHive Intelligence Systems
          </div>

          <div
            style={{
              display: "flex",
              gap: "20px"
            }}
          >

            <a href="/legal.html" style={footerLink}>
              Legal
            </a>

            <a href="/privacy.html" style={footerLink}>
              Privacy
            </a>

            <a href="/health" style={footerLink}>
              System Status
            </a>

          </div>

        </div>

      </footer>

    </div>
  );
}


function FeatureCard({ title, text }) {

  return (

    <div
      style={{
        background: "#12121A",
        border: "1px solid #1F2937",
        borderRadius: "20px",
        padding: "30px"
      }}
    >

      <h3
        style={{
          marginBottom: "16px",
          fontSize: "22px"
        }}
      >
        {title}
      </h3>

      <p
        style={{
          color: "#9CA3AF",
          lineHeight: "1.8"
        }}
      >
        {text}
      </p>

    </div>
  );
}


function StatusCard({ title, value }) {

  return (

    <div
      style={{
        background: "#0F172A",
        border: "1px solid #1E293B",
        borderRadius: "18px",
        padding: "22px"
      }}
    >

      <div
        style={{
          color: "#6B7280",
          marginBottom: "10px",
          fontSize: "14px"
        }}
      >
        {title}
      </div>

      <div
        style={{
          color: "#00D1FF",
          fontSize: "28px",
          fontWeight: "800"
        }}
      >
        {value}
      </div>

    </div>
  );
}


const footerLink = {
  color: "#9CA3AF",
  textDecoration: "none",
  fontSize: "14px"
};

export default Landing;
