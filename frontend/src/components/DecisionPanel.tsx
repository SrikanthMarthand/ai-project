import { RecommendationItem } from '../types';

interface Props {
  data: RecommendationItem[] | null;
}

export default function DecisionPanel({ data }: Props) {
  return (
    <div>
      <h2>Decision Panel</h2>
      {!data && <div className="loader">Waiting for decision data...</div>}
      {data && (
        <div className="recommendation-card">
          <ul>
            {data.map((item, index) => (
              <li key={index}>
                <strong>{item.action}</strong>: {item.detail}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
