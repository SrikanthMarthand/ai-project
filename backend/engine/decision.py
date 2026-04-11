from typing import Dict, List

from backend.engine.intent import extract_intent, module_from_file
from backend.engine.overlap import detect_overlaps
from backend.engine.simulation_future import predict_future_conflicts
from backend.engine.risk import compute_risk_summary


def build_recommendations(activities: List[Dict]) -> List[Dict]:
    recommendations: List[Dict] = []
    if not activities:
        return [{"action": "Monitor", "detail": "No activity detected yet. Keep the workspace quiet until work starts.", "priority": "LOW"}]

    risk_summary = compute_risk_summary(activities)
    overlaps = detect_overlaps(activities)
    predicted_conflicts = predict_future_conflicts(activities)
    module_activity = {}
    for activity in activities:
        module = module_from_file(activity["file_name"])
        module_activity.setdefault(module, set()).add(activity["developer_ids"][0] if "developer_ids" in activity else activity["developer_id"])

    if risk_summary.level == "HIGH":
        recommendations.append({
            "action": "Pause merges",
            "detail": "High conflict probability detected. Delay merges until active developers align their branches.",
            "priority": "HIGH",
        })
    if overlaps:
        for overlap in overlaps[:3]:
            developers = ", ".join(overlap["developer_ids"])
            recommendations.append({
                "action": "Coordinate",
                "detail": f"Developers {developers} should sync on {overlap['file_name']} due to {overlap['overlap_type']}.",
                "priority": "HIGH" if overlap["severity"] == "HIGH" else "MEDIUM",
            })
    if predicted_conflicts:
        recommendations.append({
            "action": "Review predictions",
            "detail": "Future conflict risk exists. Validate branch priorities and consider merge order optimization.",
            "priority": "MEDIUM",
        })

    for module, developers in module_activity.items():
        if len(developers) > 1:
            recommendations.append({
                "action": "Split PR",
                "detail": f"Work in module {module} is shared across developers. Split changes into smaller PRs if possible.",
                "priority": "MEDIUM",
            })
            break

    if risk_summary.level == "LOW" and not overlaps:
        recommendations.append({
            "action": "Continue",
            "detail": "Current activity is low-risk. Continue with standard collaboration patterns.",
            "priority": "LOW",
        })

    return recommendations[:6]
