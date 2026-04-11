from collections import Counter, defaultdict
from datetime import datetime, timedelta
from typing import Dict, List

from backend.models import DeveloperActivity, HotspotFile, DeveloperCollision, RiskTrendItem
from backend.engine.intent import extract_intent, module_from_file
from backend.engine.overlap import detect_overlaps
from backend.engine.risk import compute_risk_summary


class SimulationEngine:
    def __init__(self):
        self.activities: List[DeveloperActivity] = [
            DeveloperActivity(developer_id="alice", file_name="src/api.py", start_line=1, end_line=20, timestamp=datetime.utcnow() - timedelta(minutes=5)),
            DeveloperActivity(developer_id="bob", file_name="src/api.py", start_line=15, end_line=30, timestamp=datetime.utcnow() - timedelta(minutes=3)),
            DeveloperActivity(developer_id="charlie", file_name="src/utils.py", start_line=1, end_line=10, timestamp=datetime.utcnow() - timedelta(minutes=1)),
        ]
        self.history: List[DeveloperActivity] = []

    def update_activity(self, activity: DeveloperActivity) -> None:
        # Keep a compact live state, replacing prior developer-file ranges when the same developer is active again
        existing = [a for a in self.activities if not (a.developer_id == activity.developer_id and a.file_name == activity.file_name)]
        self.activities = existing + [activity]
        self.history.append(activity)

    def get_live_state(self) -> Dict:
        active_developers = sorted({activity.developer_id for activity in self.activities})
        active_files = sorted({activity.file_name for activity in self.activities})
        hotspots = self._build_hotspots()
        collision_graph = self._build_collision_graph()
        health_score = self._compute_health_score()
        risk_trend = self._build_risk_trend()
        return {
            "active_developers": active_developers,
            "active_files": active_files,
            "hotspot_files": hotspots,
            "developer_collisions": collision_graph,
            "health_score": round(health_score, 2),
            "risk_trend": risk_trend,
            "last_updated": datetime.utcnow(),
        }

    def _build_hotspots(self) -> List[HotspotFile]:
        file_activity = Counter(activity.file_name for activity in self.activities)
        hotspots = [
            HotspotFile(file_name=file_name, activity_count=count)
            for file_name, count in file_activity.most_common(6)
        ]
        return hotspots

    def _build_collision_graph(self) -> List[DeveloperCollision]:
        overlaps = detect_overlaps(self.activities)
        collisions: Dict[str, Dict] = {}
        for overlap in overlaps:
            key = tuple(sorted(overlap["developer_ids"]))
            graph_key = "::".join(key)
            collisions.setdefault(graph_key, {"developers": list(key), "risk_count": 0, "files": set()})
            collisions[graph_key]["risk_count"] += 1
            collisions[graph_key]["files"].add(overlap["file_name"])

        return [
            DeveloperCollision(developers=value["developers"], risk_count=value["risk_count"])
            for value in collisions.values()
        ]

    def _compute_health_score(self) -> float:
        if not self.activities:
            return 100.0
        active_files = len({activity.file_name for activity in self.activities})
        unique_developers = len({activity.developer_id for activity in self.activities})
        churn = sum(activity.additions + activity.deletions for activity in self.activities)
        impact = min(1.0, churn / max(1, active_files * 10))
        collision_activity = len(detect_overlaps(self.activities))
        health = max(0.0, 100.0 - (impact * 20 + collision_activity * 8 + unique_developers * 2))
        return health

    def _build_risk_trend(self) -> List[RiskTrendItem]:
        # Generate a simple trend from the last 6 updates based on history chunks
        trend = []
        recent = self.history[-18:]
        for idx in range(0, len(recent), 3):
            slice_batch = recent[idx : idx + 3]
            if slice_batch:
                risk_summary = compute_risk_summary(slice_batch)
                trend.append(RiskTrendItem(
                    timestamp=slice_batch[-1].timestamp,
                    risk_level=risk_summary.level,
                    score=risk_summary.probability
                ))
        return trend
        return trend

    def get_recent_history(self, minutes: int = 20) -> List[DeveloperActivity]:
        threshold = datetime.utcnow() - timedelta(minutes=minutes)
        return [activity for activity in self.history if activity.timestamp >= threshold]

    def snapshot_by_module(self) -> Dict[str, List[DeveloperActivity]]:
        modules: Dict[str, List[DeveloperActivity]] = defaultdict(list)
        for activity in self.activities:
            module = module_from_file(activity.file_name)
            modules[module].append(activity)
        return modules
