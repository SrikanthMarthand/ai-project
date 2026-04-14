import { SimulationState } from '../types';

interface Props {
  data: SimulationState | null;
}

export default function LiveActivityPanel({ data }: Props) {
  if (!data) {
    return (
      <div className="loader" style={{ textAlign: "center", padding: 40 }}>
        ⏳ Waiting for live GitHub activity...
      </div>
    );
  }

  const developers = data.active_developers?.length || 0;
  const files = data.active_files?.length || 0;
  const health = data.health_score || 0;

  // 🔥 CALCULATE HOTSPOTS (REALISTIC EVEN WITHOUT BACKEND)
  const hotspotMap: any = {};
  data.activity?.forEach((a: any) => {
    hotspotMap[a.file_name] = (hotspotMap[a.file_name] || 0) + 1;
  });

  const hotspotFiles = Object.entries(hotspotMap)
    .sort((a: any, b: any) => b[1] - a[1])
    .slice(0, 3);

  return (
    <div>
      <h2>🚀 Live Activity Dashboard</h2>

      {/* 🔥 TOP METRICS */}
      <div className="card-row" style={{ marginBottom: 24 }}>
        <div className="metric-card">
          <strong>👨‍💻 Active Developers</strong>
          <div className="metric-value">{developers}</div>
          <p className="subtle">Currently contributing</p>
        </div>

        <div className="metric-card">
          <strong>📂 Active Files</strong>
          <div className="metric-value">{files}</div>
          <p className="subtle">Files under modification</p>
        </div>

        <div className="metric-card">
          <strong>💚 Project Health</strong>
          <div className="metric-value">{health}%</div>
          <p className="subtle">
            {health > 80
              ? "Stable development"
              : health > 50
              ? "Moderate conflict risk"
              : "High instability detected"}
          </p>
        </div>
      </div>

      {/* 🔥 LIVE ACTIVITY STREAM */}
      <div className="list-card" style={{ marginBottom: 24 }}>
        <strong>⚡ Live Commit Stream</strong>

        <ul style={{ marginTop: 12 }}>
          {data.activity?.length > 0 ? (
            data.activity
              .slice(-6)
              .reverse()
              .map((a: any, i: number) => (
                <li key={i} style={{ marginBottom: 10 }}>
                  <span className="developer-pill">
                    {a.developer_id}
                  </span>

                  <span style={{ margin: "0 6px" }}>edited</span>

                  <span className="file-pill">
                    {a.file_name}
                  </span>

                  <span className="tag-pill">
                    +{a.additions}
                  </span>

                  <span className="tag-pill">
                    -{a.deletions}
                  </span>
                </li>
              ))
          ) : (
            <li>No live activity yet</li>
          )}
        </ul>
      </div>

      {/* 🔥 HOTSPOT FILES */}
      <div className="list-card" style={{ marginBottom: 24 }}>
        <strong>🔥 Hotspot Files</strong>

        <ul style={{ marginTop: 12 }}>
          {hotspotFiles.length > 0 ? (
            hotspotFiles.map(([file, count]: any, i) => (
              <li key={i}>
                <span className="file-pill">{file}</span>
                <span className="tag-pill">{count} edits</span>
              </li>
            ))
          ) : (
            <li>No hotspot data</li>
          )}
        </ul>
      </div>

      {/* 🔥 COLLABORATION INSIGHTS */}
      <div className="list-card">
        <strong>🤝 Developer Interaction Insights</strong>

        <ul style={{ marginTop: 12 }}>
          {developers > 1 ? (
            <li>
              Multiple developers are actively working on shared files — increased
              coordination required.
            </li>
          ) : (
            <li>✅ Single developer — low interaction risk</li>
          )}
        </ul>
      </div>
    </div>
  );
}