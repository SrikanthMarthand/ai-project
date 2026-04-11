from typing import Dict, List

from backend.engine.intent import extract_intent, analyze_intent_collisions, module_from_file
from backend.engine.overlap import detect_overlaps
from backend.models import RiskSummary


def _normalize(value: float, scale: float) -> float:
    return min(max(value / scale, 0.0), 1.0)


def compute_risk_summary(activities: List[Dict]) -> RiskSummary:
    overlaps = detect_overlaps(activities)
    intent_collisions = analyze_intent_collisions(activities)
    churn = sum(entry.get("additions", 0) + entry.get("deletions", 0) for entry in activities)
    file_overlap_score = _normalize(len({(entry["file_name"], tuple(sorted(entry["developer_ids"]))) for entry in overlaps if entry["overlap_type"] == "file-level"}), 4)
    line_overlap_score = _normalize(len([entry for entry in overlaps if entry["overlap_type"] == "line-level"]), 3)
    intent_score = _normalize(len(intent_collisions), 2)
    churn_score = _normalize(churn, max(20, len(activities) * 5))
    probability = min(1.0, line_overlap_score * 0.45 + file_overlap_score * 0.25 + intent_score * 0.2 + churn_score * 0.1)
    if probability >= 0.75:
        level = "HIGH"
    elif probability >= 0.4:
        level = "MEDIUM"
    else:
        level = "LOW"
    return RiskSummary(
        probability=round(probability, 2),
        level=level,
        score_components={
            "line_overlap": round(line_overlap_score, 2),
            "file_overlap": round(file_overlap_score, 2),
            "intent_collision": round(intent_score, 2),
            "churn": round(churn_score, 2),
            "raw_churn": churn,
        },
    )
