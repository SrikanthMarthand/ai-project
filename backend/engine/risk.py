from typing import Dict, List

from backend.engine.intent import analyze_intent_collisions
from backend.engine.overlap import detect_overlaps
from backend.models import RiskSummary


def _normalize(value: float, scale: float) -> float:
    return min(max(value / scale, 0.0), 1.0)


def compute_risk_summary(activities: List[Dict]) -> RiskSummary:
    overlaps = detect_overlaps(activities)
    intent_collisions = analyze_intent_collisions(activities)

    churn = sum(
        entry.get("additions", 0) + entry.get("deletions", 0)
        for entry in activities
    )

    # 🔥 CORE SIGNALS
    file_overlap_score = _normalize(
        len([o for o in overlaps if o["overlap_type"] == "file-level"]), 3
    )

    line_overlap_score = _normalize(
        len([o for o in overlaps if o["overlap_type"] == "line-level"]), 2
    )

    intent_score = _normalize(len(intent_collisions), 2)

    churn_score = _normalize(churn, max(10, len(activities) * 3))

    # 🔥 NEW: ACTIVITY DENSITY (makes system feel alive)
    density_score = _normalize(len(activities), 5)

    # 🔥 FINAL AI SCORING
    probability = min(
        1.0,
        (line_overlap_score * 0.4)
        + (file_overlap_score * 0.25)
        + (intent_score * 0.2)
        + (churn_score * 0.1)
        + (density_score * 0.05),
    )

    # 🔥 PREVENT DEAD UI (important)
    if probability == 0 and len(activities) > 0:
        probability = 0.15

    # 🔥 LEVEL CLASSIFICATION
    if probability >= 0.7:
        level = "HIGH"
    elif probability >= 0.35:
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
            "density": round(density_score, 2),
            "raw_churn": churn,
        },
    )