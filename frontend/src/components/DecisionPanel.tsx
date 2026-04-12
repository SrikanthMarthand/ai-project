import { RecommendationItem } from '../types';

interface Props {
  data: RecommendationItem[] | null;
}

// 🔥 priority color
const getPriorityColor = (text: string) => {
  if (text.toLowerCase().includes("immediate") || text.toLowerCase().includes("urgent")) return "red";
  if (text.toLowerCase().includes("consider")) return "orange";
  return "lime";
};

export default function DecisionPanel({ data }: Props) {

  if (!data) {
    return <div className="loader">Waiting for AI recommendations...</div>;
  }

  return (
    <div>
      <h2>AI Decision Engine</h2>

      <div className="recommendation-card">
        <ul>
          {data.length > 0 ? (
            data.map((item: any, index: number) => (
              <li key={index} style={{ marginBottom: "10px" }}>
                
                <strong style={{ color: getPriorityColor(item.action) }}>
                  {item.action}
                </strong>

                <div style={{ fontSize: "13px", opacity: 0.85 }}>
                  {item.detail}
                </div>

              </li>
            ))
          ) : (
            <li>✅ No immediate action required — system is stable</li>
          )}
        </ul>
      </div>

      {/* 🔥 extra explanation */}
      <p style={{ marginTop: 10, fontSize: "12px", opacity: 0.8 }}>
        These recommendations are generated based on detected overlaps, developer interactions, and predicted conflict risk.
      </p>
    </div>
  );
}