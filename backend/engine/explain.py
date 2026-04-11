from typing import List, Dict


def build_explanations(conflicts: List[Dict], predictions: List[Dict]) -> List[str]:
    explanations: List[str] = []
    for conflict in conflicts:
        base = []
        if "overlapping_lines" in conflict.get("reason_tags", []):
            base.append("Overlapping line ranges")
        if "shared_file" in conflict.get("reason_tags", []):
            base.append("Same file edit")
        if "same_module" in conflict.get("reason_tags", []):
            base.append("Same module affected")
        if "intent_collision" in conflict.get("reason_tags", []):
            base.append("Different developer intent detected")
        if base:
            explanations.append(f"{conflict['file_name']}: {' and '.join(base)}.")

    for prediction in predictions:
        if prediction.get("file_name"):
            explanations.append(f"Prediction for {prediction['file_name']}: {prediction['prediction']}.")
        elif prediction.get("module"):
            explanations.append(f"Prediction for module {prediction['module']}: {prediction['prediction']}.")
    if not explanations:
        explanations.append("No direct conflict signals found; the current workspace appears stable.")
    return explanations
