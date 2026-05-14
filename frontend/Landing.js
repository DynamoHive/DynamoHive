import React from "react";

export default function Landing() {
  return (
    <div
      style={{
        background: "#0B0B0F",
        color: "white",
        minHeight: "100vh",
        padding: "60px",
        fontFamily: "Arial"
      }}
    >
      <h1
        style={{
          fontSize: "48px",
          marginBottom: "10px",
          letterSpacing: "2px"
        }}
      >
        DynamoHive
      </h1>

      <p
        style={{
          color: "#888",
          fontSize: "18px",
          maxWidth: "700px",
          lineHeight: "1.6"
        }}
      >
        Real-time geopolitical intelligence, crisis detection,
        narrative monitoring and AI-driven signal analysis platform.
      </p>

      <div style={{ marginTop: "40px" }}>
        <a
          href="/dashboard"
          style={{
            color: "#00D1FF",
            textDecoration: "none",
            fontSize: "18px",
            border: "1px solid #00D1FF",
            padding: "12px 24px",
            borderRadius: "8px"
          }}
        >
          Enter Dashboard
        </a>
      </div>

      <div
        style={{
          marginTop: "80px",
          color: "#555",
          fontSize: "13px"
        }}
      >
        Experimental Intelligence Infrastructure
      </div>

      <div style={{ marginTop: "20px" }}>
        <a
          href="/legal.html"
          style={{
            color: "#666",
            marginRight: "20px",
            textDecoration: "none"
          }}
        >
          Legal
        </a>

        <a
          href="/privacy.html"
          style={{
            color: "#666",
            textDecoration: "none"
          }}
        >
          Privacy
        </a>
      </div>
    </div>
  );
}
