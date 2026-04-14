import { RiskSummary } from '../types';

interface Props {
  risk: RiskSummary | null;
}

const getRiskColor = (level?: string) => {
  if (level === "HIGH") return "#ef4444";
  if (level === "MEDIUM") return "#f59e0b";
  return "#22c55e";
};

export default function InsightsPanel({ risk }: Props) {

  if (!risk) {
    return <div className="loader">⏳ Generating AI insights...</div>;
  }

  const percent = Math.round((risk.probability || 0) * 100);
  const comp = risk.score_components || {};

  return (
    <div>
      <h2>🧠 AI Insights</h2>

      {/* 🔥 BREAKDOWN */}
      <div className="list-card" style={{ marginBottom: 18 }}>
        <strong>Risk Breakdown</strong>
        <ul>
          <li>Line Overlap: {Math.round((comp.line_overlap || 0) * 100)}%</li>
          <li>File Overlap: {Math.round((comp.file_overlap || 0) * 100)}%</li>
          <li>Intent Collision: {Math.round((comp.intent_collision || 0) * 100)}%</li>
          <li>Code Churn: {Math.round((comp.churn || 0) * 100)}%</li>
        </ul>
      </div>

      {/* 🔥 EXPLANATION */}
      <div className="list-card" style={{ marginBottom: 18 }}>
        <strong>AI Interpretation</strong>
        <ul>
          <li>Developers are working on overlapping regions of the codebase</li>
          <li>Shared file modifications increase merge complexity</li>
          <li>Higher churn indicates unstable or evolving modules</li>
        </ul>
      </div>

      {/* 🔥 OUTCOME */}
      <div className="list-card">
        <strong>Predicted Outcome</strong>

        <ul>
          <li>Risk Level: <b style={{ color: getRiskColor(risk.level) }}>{risk.level}</b></li>
          <li>Conflict Probability: {percent}%</li>
          <li>Churn Impact: {comp.raw_churn || 0} lines modified</li>
        </ul>

        <p style={{ fontSize: "12px", opacity: 0.8 }}>
          The system predicts potential merge conflicts based on real-time developer activity and recommends proactive coordination.
        </p>
      </div>
    </div>
  );
}
#akbar