
import { useEffect, useState } from "react";

export function useSignalSocket(url) {
  const [signal, setSignal] = useState(null);

  useEffect(() => {
    const ws = new WebSocket(url);
    ws.onmessage = (msg) => {
      try {
        const data = JSON.parse(msg.data);
        setSignal(data);
      } catch (e) {
        console.error("Failed to parse signal:", e);
      }
    };
    return () => ws.close();
  }, [url]);

  return signal;
}
