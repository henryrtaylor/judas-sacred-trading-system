import React, { useEffect, useState } from "react";

export default function LiveSignalFeed() {
  const [messages, setMessages] = useState([]);

  useEffect(() => {
    const ws = new WebSocket("ws://localhost:8000/ws/signals");

    ws.onmessage = (event) => {
      setMessages((prev) => [event.data, ...prev.slice(0, 9)]);
    };

    return () => ws.close();
  }, []);

  return (
    <div className="p-4 rounded-2xl shadow-md border">
      <h2 className="text-lg font-semibold mb-2">📡 Live Signal Feed</h2>
      <ul className="space-y-1 text-sm">
        {messages.map((msg, idx) => (
          <li key={idx} className="bg-gray-100 p-2 rounded">{msg}</li>
        ))}
      </ul>
    </div>
  );
}
