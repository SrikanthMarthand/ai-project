import { ConflictDetail, RiskSummary } from '../types';

interface Props {
  data: ConflictDetail[] | null;
  risk: RiskSummary | null;
}

// 🔥 Better color mapping
const getRiskColor = (level?: string) => {
  if (level === 'HIGH') return 'red';
  if (level === 'MEDIUM') return 'orange';
  return 'lime';
};

export default function ConflictPanel({ data, risk }: Props) {

  const riskPercent = Math.round((risk?.score || 0) * 100);

  return (
    <div>
      <h2>Conflict Intelligence</h2>

      {/* 🔥 Loading */}
      {!data && !risk && (
        <div className="loader">Waiting for conflict data...</div>
      )}

      {/* 🔥 Risk Summary */}
      {risk && (
        <div className="metric-card" style={{ marginBottom: 18 }}>
          <strong>Conflict Risk</strong>

          <div className="metric-value">
            {riskPercent}%
          </div>

          <span
            style={{
              color: getRiskColor(risk.level),
              fontWeight: 'bold'
            }}
          >
            {risk.level || "UNKNOWN"}
          </span>

          {/* 🔥 Extra insight */}
          <p style={{ marginTop: 6, fontSize: "12px", opacity: 0.8 }}>
            AI detected overlapping developer activity patterns
          </p>
        </div>
      )}

      {/* 🔥 Conflict Signals */}
      <div className="list-card" style={{ marginBottom: 18 }}>
        <strong>Top Conflict Signals</strong>

        <ul>
          {data && data.length > 0 ? (
            data.slice(0, 4).map((conflict: any, index: number) => (
              <li key={index}>
                <strong>{conflict.file_name || "unknown file"}</strong>
                {" — "}
                {conflict.overlap_type || "overlap"}
                {" "}
                <span style={{ color: getRiskColor(conflict.severity) }}>
                  ({conflict.severity || "LOW"})
                </span>
              </li>
            ))
          ) : (
            <li>✅ Stable workspace — no immediate conflict signals</li>
          )}
        </ul>
      </div>

      {/* 🔥 Risk Trend */}
      <div className="list-card">
        <strong>Risk Summary</strong>
        <ul>
          <li>
            Current risk level:{" "}
            <span style={{ color: getRiskColor(risk?.level) }}>
              {risk?.level || "Unknown"}
            </span>
          </li>

          <li>
            Estimated conflict probability: {riskPercent}%
          </li>
        </ul>
      </div>
    </div>
  );
}