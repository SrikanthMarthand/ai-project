import { RiskSummary } from '../types';

interface Props {
  risk: RiskSummary | null;
}

// 🔥 color helper
const getRiskColor = (level?: string) => {
  if (level === "HIGH") return "red";
  if (level === "MEDIUM") return "orange";
  return "lime";
};

export default function InsightsPanel({ risk }: Props) {

  if (!risk) {
    return <div className="loader">Waiting for AI insights...</div>;
  }

  const percent = Math.round((risk.score || 0) * 100);
  const comp = risk.score_components || {};

  return (
    <div>
      <h2>AI Insights</h2>

      {/* 🔥 Risk Breakdown */}
      <div className="list-card" style={{ marginBottom: 18 }}>
        <strong>Risk Breakdown</strong>
        <ul>
          <li>Line overlap: {Math.round((comp.line_overlap || 0) * 100)}%</li>
          <li>File overlap: {Math.round((comp.file_overlap || 0) * 100)}%</li>
          <li>Intent collision: {Math.round((comp.intent_collision || 0) * 100)}%</li>
          <li>Churn impact: {Math.round((comp.churn || 0) * 100)}%</li>
        </ul>
      </div>

      {/* 🔥 AI Explanation */}
      <div className="list-card" style={{ marginBottom: 18 }}>
        <strong>AI Explanation</strong>
        <ul>
          <li>
            Multiple developers are modifying overlapping regions of the repository.
          </li>
          <li>
            Cross-file interactions indicate tightly coupled changes.
          </li>
          <li>
            Increased code churn highlights unstable or actively evolving modules.
          </li>
        </ul>
      </div>

      {/* 🔥 Prediction + Insights */}
      <div className="list-card">
        <strong>Predicted Outcome</strong>
        <ul>
          <li>
            Risk level:{" "}
            <strong style={{ color: getRiskColor(risk.level) }}>
              {risk.level || "UNKNOWN"}
            </strong>
          </li>

          <li>
            🔮 Conflict probability:{" "}
            <strong>{percent}%</strong>
          </li>

          <li>
            Raw churn: {comp.raw_churn || 0} lines modified
          </li>
        </ul>

        {/* 🔥 Smart conclusion (VERY IMPRESSIVE) */}
        <p style={{ marginTop: 10, fontSize: "12px", opacity: 0.8 }}>
          Recommendation: Monitor high-risk files and coordinate developer activity to prevent merge conflicts.
        </p>
      </div>
    </div>
  );
}