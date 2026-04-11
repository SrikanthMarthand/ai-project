import { useEffect, useState } from "react";

export function useWebSocket(url: string) {
  const [data, setData] = useState<any>(null);

  useEffect(() => {
    const socket = new WebSocket(url);

    socket.onmessage = (event) => {
      const parsed = JSON.parse(event.data);
      setData(parsed);
    };

    return () => socket.close();
  }, [url]);

  return data;
}