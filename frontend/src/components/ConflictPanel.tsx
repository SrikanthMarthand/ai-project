import { ConflictDetail, RiskSummary } from '../types';

interface Props {
  data: ConflictDetail[] | null;
  risk: RiskSummary | null;
}

// 🔥 Color mapping
const getRiskColor = (level?: string) => {
  if (level === 'HIGH') return '#ef4444';
  if (level === 'MEDIUM') return '#f59e0b';
  return '#22c55e';
};

export default function ConflictPanel({ data, risk }: Props) {

  // ✅ FIXED (no NaN)
  const riskPercent = Math.round((risk?.probability || 0) * 100);

  return (
    <div>
      <h2>⚠️ Conflict Intelligence</h2>

      {/* 🔥 LOADING */}
      {!data && !risk && (
        <div className="loader">Waiting for conflict data...</div>
      )}

      {/* 🔥 RISK CARD */}
      {risk && (
        <div className="metric-card" style={{ marginBottom: 20 }}>
          <strong>🔥 Conflict Risk</strong>

          <div className="metric-value">
            {riskPercent}%
          </div>

          <span
            style={{
              color: getRiskColor(risk.level),
              fontWeight: 'bold',
              fontSize: "14px"
            }}
          >
            {risk.level || "UNKNOWN"}
          </span>

          {/* 🔥 AI MESSAGE */}
          <p style={{ marginTop: 8, fontSize: "13px", opacity: 0.9 }}>
            🤖 AI analyzing overlap, churn & developer interaction
          </p>

          {/* 🔥 DYNAMIC INSIGHT */}
          <p style={{ fontSize: "12px", opacity: 0.75 }}>
            {risk.level === "HIGH"
              ? "⚠️ Immediate coordination required between developers"
              : risk.level === "MEDIUM"
              ? "⚡ Moderate conflict risk detected"
              : "✅ Stable workspace — minimal conflict risk"}
          </p>
        </div>
      )}

      {/* 🔥 TOP CONFLICT SIGNALS */}
      <div className="list-card" style={{ marginBottom: 20 }}>
        <strong>🚨 Top Conflict Signals</strong>

        <ul style={{ marginTop: 10 }}>
          {data && data.length > 0 ? (
            data.slice(0, 5).map((conflict, index) => (
              <li key={index} style={{ marginBottom: 8 }}>
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
            <li>✅ No critical conflict signals detected</li>
          )}
        </ul>
      </div>

      {/* 🔥 SUMMARY */}
      <div className="list-card">
        <strong>📊 Risk Summary</strong>

        <ul style={{ marginTop: 10 }}>
          <li>
            Risk level:{" "}
            <span style={{ color: getRiskColor(risk?.level) }}>
              {risk?.level || "Unknown"}
            </span>
          </li>

          <li>
            Conflict probability: {riskPercent}%
          </li>

          <li>
            Code churn impact: {risk?.score_components?.raw_churn || 0} lines
          </li>
        </ul>
      </div>
    </div>
  );
}