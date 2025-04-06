import React, { useEffect, useState } from 'react';

export default function App() {
  const [shadow, setShadow] = useState(null);
  const [signals, setSignals] = useState([]);
  const [nlpTrades, setNlpTrades] = useState([]);

  useEffect(() => {
    fetch("/api/shadow").then(res => res.json()).then(setShadow);
    fetch("/api/signals").then(res => res.json()).then(setSignals);
    fetch("/api/nlp-trades").then(res => res.json()).then(setNlpTrades);
  }, []);

  return (
    <div className="p-6 space-y-6">
      <h1 className="text-3xl font-bold">📊 Judas Dashboard</h1>

      {shadow && (
        <div className="p-4 border rounded-xl shadow">
          <h2 className="text-xl font-semibold mb-2">🧾 Shadow Account</h2>
          <p>Balance: ${shadow.balance}</p>
          <p>Cash: ${shadow.cash}</p>
          <p>Open Trades: {shadow.open_trades}</p>
        </div>
      )}

      <div className="p-4 border rounded-xl shadow">
        <h2 className="text-xl font-semibold mb-2">📡 Live Signals</h2>
        <ul>
          {signals.map((s, i) => (
            <li key={i}>{s.symbol} — {s.signal} ({Math.round(s.confidence * 100)}%)</li>
          ))}
        </ul>
      </div>

      <div className="p-4 border rounded-xl shadow">
        <h2 className="text-xl font-semibold mb-2">🧠 NLP Trades</h2>
        <ul>
          {nlpTrades.map((t, i) => (
            <li key={i}>{t.timestamp} — {t.side} {t.symbol} ({t.reason})</li>
          ))}
        </ul>
      </div>
    </div>
  );
}
