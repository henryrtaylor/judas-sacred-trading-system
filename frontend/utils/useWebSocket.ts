import { useEffect, useState } from "react";

export const useWebSocket = (url: string) => {
  const [messages, setMessages] = useState<any[]>([]);

  useEffect(() => {
    const socket = new WebSocket(url);
    socket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setMessages((prev) => [...prev, data]);
    };
    return () => socket.close();
  }, [url]);

  return messages;
};
