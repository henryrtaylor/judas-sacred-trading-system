import { useEffect, useState } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";

export default function Dashboard() {
  const [signals, setSignals] = useState([]);
  const [trades, setTrades] = useState([]);
  const [account, setAccount] = useState({});
  const [nlp, setNlp] = useState([]);
  const [feedback, setFeedback] = useState([]);
  const [error, setError] = useState(false); // Added error state

  useEffect(() => {
    const loadData = async () => {
      try {
        const sig = await fetch(process.env.REACT_APP_API_SIGNALS || "http://localhost:8000/api/signals").then((res) => res.json());
        const trd = await fetch(process.env.REACT_APP_API_TRADES || "http://localhost:8000/api/trades").then((res) => res.json());
        const acc = await fetch(process.env.REACT_APP_API_ACCOUNT || "http://localhost:8000/api/account").then((res) => res.json());
        const headlines = await fetch("/logs/nlp_signals.json").then((res) => res.json());
        const feedbackRes = await fetch("/logs/feedback_log.json").then((res) => res.json());

        setSignals(sig);
        setTrades(trd);
        setAccount(acc);
        setNlp(headlines);
        setFeedback(feedbackRes);
        setError(false); // Reset error state on successful fetch
      } catch (err) {
        console.error("Error loading data", err);
        setError(true); // Set error state if fetching fails
      }
    };

    loadData();
    const interval = setInterval(loadData, 15000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4 p-4">
      {error && (
        <div className="col-span-1 md:col-span-2 bg-red-100 text-red-800 p-4 rounded">
          ❌ Error loading data. Please check your API or log file paths.
        </div>
      )}

      <Card>
        <CardContent>
          <h2 className="text-xl font-bold mb-2">📡 Live Signals</h2>
          {signals.length > 0 ? (
            signals.map((s, i) => (
              <div key={i} className="text-sm">
                <strong>{s.symbol}</strong>: {s.consensus} ({JSON.stringify(s.votes)})
              </div>
            ))
          ) : (
            <div className="text-sm text-gray-500">No signals available.</div>
          )}
        </CardContent>
      </Card>

      <Card>
        <CardContent>
          <h2 className="text-xl font-bold mb-2">📈 Trade Journal</h2>
          {trades.length > 0 ? (
            trades.slice(-10).reverse().map((t, i) => (
              <div key={i} className="text-sm">
                [{t.timestamp}] {t.side} {t.qty} {t.symbol} @ {t.price} — {t.reason}
              </div>
            ))
          ) : (
            <div className="text-sm text-gray-500">No trades available.</div>
          )}
        </CardContent>
      </Card>

      <Card className="col-span-1 md:col-span-2">
        <CardContent>
          <h2 className="text-xl font-bold mb-2">💰 Account Snapshot</h2>
          {Object.keys(account).length > 0 ? (
            <pre className="text-sm bg-black/10 p-2 rounded">
              {JSON.stringify(account, null, 2)}
            </pre>
          ) : (
            <div className="text-sm text-gray-500">No account data available.</div>
          )}
        </CardContent>
      </Card>

      <Card className="col-span-1 md:col-span-2">
        <CardContent>
          <h2 className="text-xl font-bold mb-2">🗞️ NLP News Signals</h2>
          {nlp.length > 0 ? (
            nlp.map((entry, i) => (
              <div key={i} className="text-sm mb-1">
                <strong>{entry.symbol}</strong>: {entry.signal} ({(entry.confidence * 100).toFixed(0)}%) — {entry.reason}<br />
                <em className="text-xs text-gray-600">{entry.headline}</em>
              </div>
            ))
          ) : (
            <div className="text-sm text-gray-500">No NLP signals available.</div>
          )}
        </CardContent>
      </Card>

      <Card className="col-span-1 md:col-span-2">
        <CardContent>
          <h2 className="text-xl font-bold mb-2">📉 Signal Feedback: PnL Timeline</h2>
          {feedback.length > 0 ? (
            <ResponsiveContainer width="100%" height={200}>
              <LineChart data={feedback.map((f, i) => ({ name: i + 1, pnl: f.pnl }))}>
                <XAxis dataKey="name" />
                <YAxis domain={[dataMin => dataMin - 10, dataMax => dataMax + 10]} />
                <Tooltip />
                <Line type="monotone" dataKey="pnl" stroke="#4ade80" strokeWidth={2} />
              </LineChart>
            </ResponsiveContainer>
          ) : (
            <div className="text-sm text-gray-500">No feedback data available.</div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
