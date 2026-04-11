from backend.engine.decision import build_recommendations
from backend.engine.explain import build_explanations
from backend.engine.intent import analyze_intent_collisions, extract_intent, module_from_file
from backend.engine.overlap import detect_overlaps
from backend.engine.risk import compute_risk_summary
from backend.engine.simulation import SimulationEngine
from backend.engine.simulation_future import predict_future_conflicts

__all__ = [
    "SimulationEngine",
    "detect_overlaps",
    "extract_intent",
    "module_from_file",
    "analyze_intent_collisions",
    "compute_risk_summary",
    "predict_future_conflicts",
    "build_explanations",
    "build_recommendations",
]
