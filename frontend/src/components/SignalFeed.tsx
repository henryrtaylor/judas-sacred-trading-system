import { useEffect, useState } from "react";
import { connectWebSocket, disconnectWebSocket } from "@/lib/ws";

export default function SignalFeed() {
  const [signals, setSignals] = useState<any[]>([]);

  useEffect(() => {
    connectWebSocket((msg) => {
      setSignals((prev) => [msg, ...prev]);
    });

    return () => disconnectWebSocket();
  }, []);

  return (
    <div className="p-4">
      <h2 className="text-xl font-bold mb-2">📡 Live Signals</h2>
      <ul className="space-y-2">
        {signals.map((signal, idx) => (
          <li key={idx} className="bg-gray-100 p-2 rounded shadow">
            <strong>{signal.symbol}</strong>: {signal.signal}
          </li>
        ))}
      </ul>
    </div>
  );
}