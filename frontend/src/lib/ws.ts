let socket: WebSocket | null = null;

export const connectWebSocket = (onMessage: (msg: any) => void) => {
  socket = new WebSocket("ws://localhost:8000/ws/signals");

  socket.onopen = () => console.log("📡 WebSocket connected");
  socket.onmessage = (event) => {
    const data = JSON.parse(event.data);
    console.log("📥 WebSocket message received:", data);
    onMessage(data);
  };
  socket.onerror = (err) => console.error("❌ WebSocket error", err);
  socket.onclose = () => console.warn("🔌 WebSocket closed");
};

export const disconnectWebSocket = () => {
  if (socket) {
    socket.close();
  }
};