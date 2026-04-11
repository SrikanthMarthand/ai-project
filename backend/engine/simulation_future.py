from collections import Counter
from typing import Dict, List

from backend.engine.intent import extract_intent, module_from_file
from backend.engine.overlap import detect_overlaps


def predict_future_conflicts(activities: List[Dict]) -> List[Dict]:
    predictions = []
    overlap_records = detect_overlaps(activities)
    file_counts = Counter(activity["file_name"] for activity in activities)
    module_counts = Counter(module_from_file(activity["file_name"]) for activity in activities)

    for conflict in overlap_records:
        probability = 0.6 if conflict["overlap_type"] == "file-level" else 0.85
        predictions.append({
            "file_name": conflict["file_name"],
            "developer_ids": conflict["developer_ids"],
            "prediction": "Immediate merge risk",
            "confidence": round(probability, 2),
            "drivers": conflict["reason_tags"],
        })

    for file_name, count in file_counts.items():
        if count >= 3:
            predictions.append({
                "file_name": file_name,
                "prediction": "Hotspot: file is edited by multiple developers",
                "confidence": 0.7,
                "drivers": ["hotspot_file", "multi-developer"],
            })

    for module, count in module_counts.items():
        if count >= 2:
            predictions.append({
                "module": module,
                "prediction": "Module-level churn may trigger intent drift",
                "confidence": 0.5,
                "drivers": ["module_churn", "intent_sensitivity"],
            })
    return predictions
