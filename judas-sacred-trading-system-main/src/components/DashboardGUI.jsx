import React from "react";

const mockPortfolio = [
  { symbol: "NVDA", actual: 0.12, target: 0.20 },
  { symbol: "QQQ", actual: 0.25, target: 0.25 },
  { symbol: "SCHD", actual: 0.18, target: 0.30 },
  { symbol: "JEPI", actual: 0.15, target: 0.10 },
  { symbol: "CASH", actual: 0.30, target: 0.15 }
];

export default function DashboardGUI() {
  return (
    <div style={{ padding: "2rem", maxWidth: "600px", margin: "auto" }}>
      <h2 style={{ fontSize: "1.5rem", marginBottom: "1rem" }}>
        📊 Judas Portfolio Alignment
      </h2>
      {mockPortfolio.map(({ symbol, actual, target }) => {
        const delta = actual - target;
        const deltaPct = (delta * 100).toFixed(2);
        const barWidth = Math.min(Math.max(actual * 100, 0), 100);
        const barColor = Math.abs(delta) < 0.01 ? "green" : delta > 0 ? "red" : "orange";

        return (
          <div key={symbol} style={{ marginBottom: "1.5rem" }}>
            <div style={{ display: "flex", justifyContent: "space-between" }}>
              <strong>{symbol}</strong>
              <span
                style={{
                  backgroundColor: barColor,
                  color: "white",
                  padding: "2px 8px",
                  borderRadius: "5px",
                  fontSize: "0.8rem"
                }}
              >
                Drift: {deltaPct}%
              </span>
            </div>
            <div style={{ height: "8px", background: "#eee", borderRadius: "4px", marginTop: "4px" }}>
              <div
                style={{
                  width: `${barWidth}%`,
                  height: "100%",
                  background: barColor,
                  borderRadius: "4px"
                }}
              />
            </div>
            <div style={{ fontSize: "0.75rem", color: "#666", marginTop: "4px" }}>
              Target: {(target * 100).toFixed(1)}% | Actual: {(actual * 100).toFixed(1)}%
            </div>
          </div>
        );
      })}
    </div>
  );
}
