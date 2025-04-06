import React, { useEffect, useState } from 'react';

export default function LiveSignalFeed() {
  const [messages, setMessages] = useState([]);

  useEffect(() => {
    const socket = new WebSocket(import.meta.env.VITE_WS_URL || "ws://localhost:8000/ws/signals");

    socket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setMessages((prev) => [data, ...prev.slice(0, 20)]);
    };

    return () => socket.close();
  }, []);

  return (
    <div className="p-4">
      <h2 className="text-xl font-bold mb-4">📡 Live Signal Feed</h2>
      <ul className="space-y-2">
        {messages.map((msg, idx) => (
          <li key={idx} className="p-3 rounded-lg shadow border">
            <div><strong>Symbol:</strong> {msg.symbol}</div>
            <div><strong>Action:</strong> {msg.action}</div>
            <div><strong>Confidence:</strong> {msg.confidence}</div>
            <div><strong>Time:</strong> {new Date(msg.timestamp).toLocaleString()}</div>
          </li>
        ))}
      </ul>
    </div>
  );
}