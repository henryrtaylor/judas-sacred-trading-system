import React from "react";
import { useSignalWebSocket } from "./useSignalWebSocket";

export default function LiveFeed() {
  const signal = useSignalWebSocket();

  return (
    <div className="p-4 border rounded bg-white shadow-xl">
      <h2 className="text-lg font-bold mb-2">📡 Live Signal Feed</h2>
      {signal ? (
        <div>
          <p><strong>Symbol:</strong> {signal.symbol}</p>
          <p><strong>Action:</strong> {signal.action}</p>
          <p><strong>Confidence:</strong> {Math.round(signal.confidence * 100)}%</p>
          <p><strong>Timestamp:</strong> {signal.timestamp}</p>
        </div>
      ) : (
        <p>Waiting for signal...</p>
      )}
    </div>
  );
}
