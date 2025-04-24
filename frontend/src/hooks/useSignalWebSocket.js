import { useEffect, useState } from "react";

export function useSignalWebSocket() {
  const [signal, setSignal] = useState(null);

  useEffect(() => {
    const ws = new WebSocket("ws://localhost:8000/ws/signals");
    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        setSignal(data);
      } catch (e) {
        console.error("Invalid signal:", e);
      }
    };
    ws.onerror = (err) => console.error("WebSocket error:", err);
    return () => ws.close();
  }, []);

  return signal;
}
