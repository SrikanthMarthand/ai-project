import { useEffect, useRef, useState } from 'react';
import LiveActivityPanel from './components/LiveActivityPanel';
import ConflictPanel from './components/ConflictPanel';
import InsightsPanel from './components/InsightsPanel';
import DecisionPanel from './components/DecisionPanel';

function App() {
  const [data, setData] = useState<any>(null);
  const [isConnected, setIsConnected] = useState(false);
  const socketRef = useRef<WebSocket | null>(null);

  useEffect(() => {
    const socket = new WebSocket("ws://localhost:8000/ws");
    socketRef.current = socket;

    socket.onopen = () => setIsConnected(true);

    socket.onclose = () => {
      setIsConnected(false);
      console.log("Socket closed");
    };

    socket.onmessage = (event) => {
      try {
        const parsed = JSON.parse(event.data);
        setData(parsed);
      } catch (e) {
        console.log("Parse error", e);
      }
    };

    return () => socket.close();
  }, []);

  return (
    <div className="app-container">

      {/* 🔥 HEADER */}
      <header className="header">
        <div>
          <h1>⚡ DevTwin AI</h1>
          <p>Real-Time Conflict Intelligence Platform</p>
        </div>

        <div className={`status ${isConnected ? "live" : "offline"}`}>
          {isConnected ? "LIVE" : "OFFLINE"}
        </div>
      </header>

      {!data ? (
        <div className="center">Connecting to AI engine...</div>
      ) : (
        <>
          {/* 🔥 KPI SECTION */}
          <div className="kpi-container">

            <div className="kpi-card">
              <h4>Active Developers</h4>
              <p>{data.active_developers?.length || 0}</p>
            </div>

            <div className="kpi-card">
              <h4>Active Files</h4>
              <p>{data.active_files?.length || 0}</p>
            </div>

            <div className="kpi-card danger">
              <h4>Conflict Risk</h4>
              <p>{Math.round((data.risk?.probability || 0) * 100)}%</p>
            </div>

            <div className="kpi-card success">
              <h4>Project Health</h4>
              <p>{data.health_score}%</p>
            </div>

          </div>

          {/* 🔥 MAIN GRID */}
          <div className="dashboard-grid">

            <div className="panel large">
              <LiveActivityPanel data={data} />
            </div>

            <div className="panel">
              <ConflictPanel data={data.overlap} risk={data.risk} />
            </div>

            <div className="panel">
              <InsightsPanel risk={data.risk} />
            </div>

            <div className="panel large">
              <DecisionPanel data={data.decision} />
            </div>

          </div>

          {/* 🔥 FOOTER */}
          <div className="footer">
            Last updated: {new Date(data.last_updated).toLocaleTimeString()}
          </div>
        </>
      )}
    </div>
  );
}
export default App;