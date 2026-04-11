import { SimulationState } from '../types';

interface Props {
  data: SimulationState | null;
}

export default function LiveActivityPanel({ data }: Props) {
  return (
    <div>
      <h2>Live Activity Dashboard</h2>
      {!data && <div className="loader">Waiting for live data...</div>}
      {data && (
        <>
          <div className="card-row" style={{ marginBottom: 18 }}>
            <div className="metric-card">
              <strong>Active developers</strong>
              <div className="metric-value">{data.active_developers.length}</div>
            </div>
            <div className="metric-card">
              <strong>Active files</strong>
              <div className="metric-value">{data.active_files.length}</div>
            </div>
            <div className="metric-card">
              <strong>Project health</strong>
              <div className="metric-value">{data.health_score}%</div>
            </div>
          </div>

          <div className="list-card" style={{ marginBottom: 18 }}>
            <strong>Hotspot files</strong>
            <ul>
              {data.hotspot_files.map((item: any) => (
                <li key={item.file_name}>
                  <span className="file-pill">{item.file_name}</span> {item.activity_count} active edits
                </li>
              ))}
            </ul>
          </div>

          <div className="list-card">
            <strong>Developer collisions</strong>
            <ul>
              {data.developer_collisions.length > 0 ? (
                data.developer_collisions.map((collision: any) => (
                  <li key={collision.developers.join('-')}>
                    <span className="developer-pill">{collision.developers.join(', ')}</span>
                    <span className="tag-pill">{collision.risk_count} interaction(s)</span>
                  </li>
                ))
              ) : (
                <li>No collisions detected</li>
              )}
            </ul>
          </div>
        </>
      )}
    </div>
  );
}
