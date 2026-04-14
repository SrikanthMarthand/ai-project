import { RecommendationItem } from '../types';

interface Props {
  data: RecommendationItem[] | null;
}

const getPriorityColor = (text: string) => {
  if (text.toLowerCase().includes("immediate")) return "#ef4444";
  if (text.toLowerCase().includes("coordinate")) return "#f59e0b";
  return "#22c55e";
};

export default function DecisionPanel({ data }: Props) {

  if (!data) {
    return <div className="loader">⏳ Waiting for AI decisions...</div>;
  }

  return (
    <div>
      <h2>🤖 AI Decision Engine</h2>

      <div className="recommendation-card">
        <ul>
          {data.length > 0 ? (
            data.map((item, i) => (
              <li key={i} style={{ marginBottom: 12 }}>
                <strong style={{ color: getPriorityColor(item.action) }}>
                  {item.action}
                </strong>

                <div style={{ fontSize: "13px", opacity: 0.85 }}>
                  {item.detail}
                </div>
              </li>
            ))
          ) : (
            <li>✅ No action required — system stable</li>
          )}
        </ul>
      </div>

      <p style={{ marginTop: 10, fontSize: "12px", opacity: 0.8 }}>
        AI recommendations are generated from conflict prediction signals and developer interaction patterns.
      </p>
    </div>
  );
}