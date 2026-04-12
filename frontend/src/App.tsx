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
    const socket = new WebSocket("ws://127.0.0.1:8000/ws");
    socketRef.current = socket;

    socket.onopen = () => setIsConnected(true);
    socket.onclose = () => setIsConnected(false);

    socket.onmessage = (event) => {
      const parsed = JSON.parse(event.data);
      setData(parsed);
    };

    return () => socket.close();
  }, []);

  return (
    <div className="app">

      {/* 🔥 SIDEBAR */}
      <aside className="sidebar">
        <h2>⚡ DevTwin</h2>
        <nav>
          <p className="active">Dashboard</p>
          <p>Repositories</p>
          <p>Insights</p>
          <p>Settings</p>
        </nav>
      </aside>

      {/* 🔥 MAIN */}
      <main className="main">

        {/* 🔥 HEADER */}
        <div className="topbar">
          <h1>Real-Time Conflict Intelligence</h1>
          <div className={`status ${isConnected ? "live" : "offline"}`}>
            {isConnected ? "LIVE" : "OFFLINE"}
          </div>
        </div>

        {!data ? (
          <div className="center">Connecting to AI engine...</div>
        ) : (
          <>
            {/* 🔥 KPI CARDS */}
            <div className="kpi-row">
              <div className="kpi glow">
                <h4>Developers</h4>
                <p>{data.active_developers.length}</p>
              </div>

              <div className="kpi glow">
                <h4>Files</h4>
                <p>{data.active_files.length}</p>
              </div>

              <div className="kpi glow danger">
                <h4>Conflict Risk</h4>
                <p>{Math.round(data.risk.score * 100)}%</p>
              </div>

              <div className="kpi glow success">
                <h4>Health</h4>
                <p>{data.health_score}%</p>
              </div>
            </div>

            {/* 🔥 MAIN GRID */}
            <div className="grid">
              <div className="card glass">
                <LiveActivityPanel data={data} />
              </div>

              <div className="card glass">
                <ConflictPanel data={data.overlap} risk={data.risk} />
              </div>

              <div className="card glass">
                <InsightsPanel risk={data.risk} />
              </div>

              <div className="card glass">
                <DecisionPanel data={data.decision} />
              </div>
            </div>
          </>
        )}

      </main>
    </div>
  );
}

export default App;