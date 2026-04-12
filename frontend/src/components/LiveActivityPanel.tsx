import { SimulationState } from '../types';

interface Props {
  data: SimulationState | null;
}

export default function LiveActivityPanel({ data }: Props) {
  if (!data) {
    return <div className="loader">Waiting for live data...</div>;
  }

  return (
    <div>
      <h2>Live Activity Dashboard</h2>

      <div className="card-row" style={{ marginBottom: 18 }}>
        <div className="metric-card">
          <strong>Active developers</strong>
          <div className="metric-value">
            {data.active_developers?.length || 0}
          </div>
        </div>

        <div className="metric-card">
          <strong>Active files</strong>
          <div className="metric-value">
            {data.active_files?.length || 0}
          </div>
        </div>

        <div className="metric-card">
          <strong>Project health</strong>
          <div className="metric-value">
            {data.health_score || 0}%
          </div>
        </div>
      </div>

      {/* 🔥 SAFE HOTSPOT FILES */}
      <div className="list-card" style={{ marginBottom: 18 }}>
        <strong>Hotspot files</strong>
        <ul>
          {data.hotspot_files?.length > 0 ? (
            data.hotspot_files.map((item: any, i: number) => (
              <li key={i}>
                <span className="file-pill">{item.file_name}</span>{" "}
                {item.activity_count} active edits
              </li>
            ))
          ) : (
            <li>No hotspot data</li>
          )}
        </ul>
      </div>

      {/* 🔥 SAFE COLLISIONS */}
      <div className="list-card">
        <strong>Developer collisions</strong>
        <ul>
          {data.developer_collisions?.length > 0 ? (
            data.developer_collisions.map((collision: any, i: number) => (
              <li key={i}>
                <span className="developer-pill">
                  {collision.developers?.join(', ') || "N/A"}
                </span>
                <span className="tag-pill">
                  {collision.risk_count || 0} interaction(s)
                </span>
              </li>
            ))
          ) : (
            <li>No collisions detected</li>
          )}
        </ul>
      </div>
    </div>
  );
}