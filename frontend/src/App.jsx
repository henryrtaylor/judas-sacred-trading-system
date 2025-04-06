
import React from "react";
import { useSignalSocket } from "./useSignalSocket";

export default function App() {
  const signal = useSignalSocket("ws://localhost:8000/ws/signals");

  return (
    <div className="p-6 font-mono text-white bg-black min-h-screen">
      <h1 className="text-2xl mb-4">📡 Live Judas Signals</h1>
      <pre>{signal ? JSON.stringify(signal, null, 2) : "Waiting for signal..."}</pre>
    </div>
  );
}
