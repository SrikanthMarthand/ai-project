import { ConflictDetail, RiskSummary } from '../types';

interface Props {
  data: ConflictDetail[] | null;
  risk: RiskSummary | null;
}

const getRiskColor = (level?: string) => {
  if (level === 'HIGH') return '#ef4444';
  if (level === 'MEDIUM') return '#f59e0b';
  return '#22c55e';
};

export default function ConflictPanel({ data, risk }: Props) {

  const riskPercent = Math.round((risk?.probability || 0) * 100);

  return (
    <div>
      <h2>⚠️ Conflict Intelligence</h2>

      {/* 🔥 RISK CARD */}
      {risk && (
        <div className="metric-card" style={{ marginBottom: 20 }}>
          <strong>🔥 Conflict Risk</strong>

          <div className="metric-value">{riskPercent}%</div>

          <span style={{
            color: getRiskColor(risk.level),
            fontWeight: 'bold'
          }}>
            {risk.level}
          </span>

          <p style={{ fontSize: "12px", opacity: 0.8, marginTop: 6 }}>
            AI analyzing overlap, developer interaction, and code churn
          </p>

          <p style={{ fontSize: "12px", opacity: 0.8 }}>
            {risk.level === "HIGH"
              ? "⚠️ High probability of merge conflict — immediate coordination recommended"
              : risk.level === "MEDIUM"
              ? "⚡ Moderate risk detected due to shared file activity"
              : "✅ Low risk — development flow is stable"}
          </p>
        </div>
      )}

      {/* 🔥 SIGNALS */}
      <div className="list-card" style={{ marginBottom: 20 }}>
        <strong>🚨 Conflict Signals</strong>

        <ul style={{ marginTop: 10 }}>
          {data && data.length > 0 ? (
            data.slice(0, 5).map((c, i) => (
              <li key={i}>
                <span className="file-pill">{c.file_name}</span>

                <span style={{ marginLeft: 6 }}>
                  {c.overlap_type}
                </span>

                <span style={{
                  marginLeft: 6,
                  color: getRiskColor(c.severity)
                }}>
                  {c.severity}
                </span>
              </li>
            ))
          ) : (
            <li>✅ No conflict signals detected</li>
          )}
        </ul>
      </div>

      {/* 🔥 SUMMARY */}
      <div className="list-card">
        <strong>📊 Summary</strong>

        <ul>
          <li>Risk Level: <b style={{ color: getRiskColor(risk?.level) }}>{risk?.level}</b></li>
          <li>Probability: {riskPercent}%</li>
          <li>Code Churn: {risk?.score_components?.raw_churn || 0} lines</li>
        </ul>
      </div>
    </div>
  );
}