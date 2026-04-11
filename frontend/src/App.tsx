import { useEffect, useRef, useState } from 'react';
import { SimulationState, ConflictDetail, RecommendationItem, RiskSummary } from './types';
import LiveActivityPanel from './components/LiveActivityPanel';
import ConflictPanel from './components/ConflictPanel';
import InsightsPanel from './components/InsightsPanel';
import DecisionPanel from './components/DecisionPanel';

function App() {
  const [data, setData] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);
  const [isConnected, setIsConnected] = useState(false);
  const socketRef = useRef<WebSocket | null>(null);
  const reconnectRef = useRef<number | null>(null);
  const wsUrl = "ws://127.0.0.1:8000/ws";

  useEffect(() => {
    const connect = () => {
      if (socketRef.current && socketRef.current.readyState !== WebSocket.CLOSED) {
        return;
      }

      const socket = new WebSocket(wsUrl);
      socketRef.current = socket;
      console.log("DevTwin: attempting WebSocket connect to", wsUrl);

      socket.onopen = () => {
        console.log("DevTwin: WebSocket open");
        setIsConnected(true);
        setError(null);
      };

      socket.onmessage = (event) => {
        try {
          const parsed = JSON.parse(event.data);
          setData(parsed);
        } catch (err) {
          console.error("DevTwin: invalid WebSocket message", err, event.data);
        }
      };

      socket.onclose = (event) => {
        console.log("DevTwin: WebSocket closed", event.code, event.reason, event.wasClean);
        setIsConnected(false);
        if (!event.wasClean) {
          setError("WebSocket disconnected, retrying...");
        }
        if (reconnectRef.current) {
          window.clearTimeout(reconnectRef.current);
        }
        reconnectRef.current = window.setTimeout(connect, 1000);
      };

      socket.onerror = (event) => {
        console.error("DevTwin: WebSocket error", event);
        setError("WebSocket connection error");
        setIsConnected(false);
      };
    };

    connect();

    return () => {
      if (reconnectRef.current) {
        window.clearTimeout(reconnectRef.current);
      }
      if (socketRef.current) {
        socketRef.current.close();
      }
    };
  }, []);

  return (
    <div className="app-shell">
      <header className="header">
        <h1 className="title">DevTwin AI</h1>
        <p className="subtitle">
          Real-Time Intent-Aware Repository Intelligence Platform
        </p>
        <span style={{ color: isConnected ? "lime" : "red" }}>
          {isConnected ? "🟢 LIVE" : "🔴 CONNECTING..."}
        </span>
      </header>

      {error && <p style={{ color: "red" }}>{error}</p>}

      <div className="grid-dashboard">

        <section className="panel" style={{ gridColumn: 'span 8' }}>
          <LiveActivityPanel data={data} />
        </section>

        <section className="panel" style={{ gridColumn: 'span 4' }}>
          <ConflictPanel data={data?.overlap} risk={data?.risk} />
        </section>

        <section className="panel" style={{ gridColumn: 'span 5' }}>
          <InsightsPanel risk={data?.risk} />
        </section>

        <section className="panel" style={{ gridColumn: 'span 7' }}>
          <DecisionPanel data={data?.decision} />
        </section>

      </div>
    </div>
  );
}

export default App;