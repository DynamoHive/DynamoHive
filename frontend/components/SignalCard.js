import React from "react";

import theme from "../theme";


export default function SignalCard({ signal }) {

  const severityColor =
    signal?.severity === "high"
      ? theme.colors.high
      : signal?.severity === "medium"
      ? theme.colors.medium
      : theme.colors.low;

  return (

    <div
      style={{
        ...theme.components.card,
        boxShadow: theme.shadows.card,
        transition: theme.transitions.default
      }}
    >

      {/* HEADER */}
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          marginBottom: "16px"
        }}
      >

        <div
          style={{
            color: theme.colors.primary,
            fontSize: "13px",
            letterSpacing: "1px",
            textTransform: "uppercase"
          }}
        >
          SIGNAL
        </div>

        <div
          style={{
            background: severityColor,
            color: "#000",
            padding: "6px 12px",
            borderRadius: theme.radius.pill,
            fontSize: "12px",
            fontWeight: "bold",
            textTransform: "uppercase"
          }}
        >
          {signal?.severity || "low"}
        </div>

      </div>


      {/* TOPIC */}
      <h3
        style={{
          color: theme.colors.text,
          marginBottom: "14px",
          fontSize: "22px",
          lineHeight: "1.4"
        }}
      >
        {signal?.topic || "Unknown signal"}
      </h3>


      {/* TEXT */}
      <p
        style={{
          color: theme.colors.muted,
          lineHeight: "1.7",
          marginBottom: "20px"
        }}
      >
        {signal?.text || "No description available"}
      </p>


      {/* METRICS */}
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(3,1fr)",
          gap: "12px",
          marginBottom: "20px"
        }}
      >

        <Metric
          label="Score"
          value={signal?.score ?? 0}
        />

        <Metric
          label="Confidence"
          value={signal?.confidence ?? 0}
        />

        <Metric
          label="Sources"
          value={
            signal?.sources?.length || 0
          }
        />

      </div>


      {/* FOOTER */}
      <div
        style={{
          borderTop: `1px solid ${theme.colors.border}`,
          paddingTop: "14px",
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          color: theme.colors.dim,
          fontSize: "13px"
        }}
      >

        <div>
          {signal?.signal_id || "N/A"}
        </div>

        <div>
          {signal?.timestamp || "Unknown"}
        </div>

      </div>

    </div>
  );
}


function Metric({ label, value }) {

  return (

    <div
      style={{
        background: theme.colors.surfaceAlt,
        padding: "12px",
        borderRadius: "12px",
        border: `1px solid ${theme.colors.border}`
      }}
    >

      <div
        style={{
          color: theme.colors.dim,
          fontSize: "12px",
          marginBottom: "6px"
        }}
      >
        {label}
      </div>

      <div
        style={{
          color: theme.colors.text,
          fontWeight: "bold",
          fontSize: "18px"
        }}
      >
        {value}
      </div>

    </div>
  );
}
