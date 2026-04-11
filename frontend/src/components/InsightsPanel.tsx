import { RiskSummary } from '../types';

interface Props {
  risk: RiskSummary | null;
}

export default function InsightsPanel({ risk }: Props) {
  return (
    <div>
      <h2>AI Insights</h2>
      {!risk && <div className="loader">Waiting for risk analysis...</div>}
      {risk && (
        <>
          <div className="list-card" style={{ marginBottom: 18 }}>
            <strong>Risk breakdown</strong>
            <ul>
              <li>Line overlap contribution: {risk.score_components.line_overlap * 100}%</li>
              <li>File overlap contribution: {risk.score_components.file_overlap * 100}%</li>
              <li>Intent collision contribution: {risk.score_components.intent_collision * 100}%</li>
              <li>Churn impact: {risk.score_components.churn * 100}%</li>
            </ul>
          </div>

          <div className="list-card">
            <strong>Insights</strong>
            <ul>
              <li>Risk level: {risk.level}</li>
              <li>Overall probability: {risk.probability * 100}%</li>
              <li>Raw churn: {risk.score_components.raw_churn} lines</li>
            </ul>
          </div>
        </>
      )}
    </div>
  );
}
