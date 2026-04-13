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
              ? "Moderate risk"
              : "High instability"}
          </p>
        </div>
      </div>

      {/* 🔥 LIVE ACTIVITY FEED (VERY IMPORTANT) */}
      <div className="list-card" style={{ marginBottom: 24 }}>
        <strong>⚡ Live Developer Activity</strong>

        <ul style={{ marginTop: 12 }}>
          {data.activity?.length > 0 ? (
            data.activity.slice(0, 6).map((a: any, i: number) => (
              <li key={i} style={{ marginBottom: 10 }}>
                <span className="developer-pill">
                  {a.developer_id}
                </span>

                <span className="file-pill">
                  {a.file_name}
                </span>

                <span style={{ fontSize: "12px", opacity: 0.7 }}>
                  +{a.additions} / -{a.deletions}
                </span>
              </li>
            ))
          ) : (
            <li>No live activity</li>
          )}
        </ul>
      </div>

      {/* 🔥 HOTSPOT FILES */}
      <div className="list-card" style={{ marginBottom: 24 }}>
        <strong>🔥 Hotspot Files (High Activity)</strong>

        <ul style={{ marginTop: 12 }}>
          {data.hotspot_files?.length > 0 ? (
            data.hotspot_files.map((item: any, i: number) => (
              <li key={i}>
                <span className="file-pill">{item.file_name}</span>
                <span className="tag-pill">
                  {item.activity_count} edits
                </span>
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
          {data.developer_collisions?.length > 0 ? (
            data.developer_collisions.map((collision: any, i: number) => (
              <li key={i}>
                <span className="developer-pill">
                  {collision.developers?.join(', ') || "N/A"}
                </span>

                <span className="tag-pill">
                  {collision.risk_count || 0} overlaps
                </span>
              </li>
            ))
          ) : (
            <li>✅ No risky interactions detected</li>
          )}
        </ul>
      </div>
    </div>
  );
}