import { ConflictDetail, RiskSummary } from '../types';

interface Props {
  data: ConflictDetail[] | null;
  risk: RiskSummary | null;
}

const severityClass = (level: string) => {
  if (level === 'HIGH') return 'status-high';
  if (level === 'MEDIUM') return 'status-medium';
  return 'status-low';
};

export default function ConflictPanel({ data, risk }: Props) {
  return (
    <div>
      <h2>Conflict Intelligence</h2>
      {!data && !risk && <div className="loader">Waiting for conflict data...</div>}
      {risk && (
        <div className="metric-card" style={{ marginBottom: 18 }}>
          <strong>Risk score</strong>
          <div className="metric-value">{risk.probability * 100}%</div>
          <span className={`status-pill ${severityClass(risk.level)}`}>{risk.level}</span>
        </div>
      )}

      <div className="list-card" style={{ marginBottom: 18 }}>
        <strong>Top conflict signals</strong>
        <ul>
          {data && data.length > 0 ? (
            data.slice(0, 4).map((conflict, index) => (
              <li key={`${conflict.file_name}-${index}`}>
                <strong>{conflict.file_name}</strong> — {conflict.overlap_type} ({conflict.severity})
              </li>
            ))
          ) : (
            <li>Stable workspace — no immediate conflict signals.</li>
          )}
        </ul>
      </div>

      <div className="list-card">
        <strong>Risk trend</strong>
        <ul>
          <li>Current risk level: {risk?.level || 'Unknown'}</li>
        </ul>
      </div>
    </div>
  );
}
