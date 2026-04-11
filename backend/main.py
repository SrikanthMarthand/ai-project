from datetime import datetime
from typing import List

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
import asyncio
from websockets.exceptions import ConnectionClosedOK

from backend.engine.decision import build_recommendations
from backend.engine.explain import build_explanations
from backend.engine.intent import analyze_intent_collisions, extract_intent
from backend.engine.risk import compute_risk_summary
from backend.engine.simulation import SimulationEngine
from backend.engine.simulation_future import predict_future_conflicts
from backend.engine.overlap import detect_overlaps
from backend.models import AnalysisResponse, ConflictDetail, DeveloperActivity, RecommendationItem, RiskSummary, SimulationState

app = FastAPI(
    title="DevTwin AI",
    description="Real-Time Intent-Aware Repository Intelligence Platform",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = SimulationEngine()


@app.get("/health")
def health_check() -> dict:
    return {"status": "ok", "service": "DevTwin AI"}


@app.post("/simulate")
def simulate_activity(activity: DeveloperActivity) -> dict:
    engine.update_activity(activity)
    return {"status": "updated", "developer_id": activity.developer_id, "file_name": activity.file_name}


@app.get("/state")
def get_state() -> SimulationState:
    state = engine.get_live_state()
    return SimulationState(
        active_developers=state["active_developers"],
        active_files=state["active_files"],
        hotspot_files=state["hotspot_files"],
        developer_collisions=state["developer_collisions"],
        health_score=state["health_score"],
        risk_trend=state["risk_trend"],
        last_updated=state["last_updated"],
    )


@app.post("/analyze")
def analyze() -> AnalysisResponse:
    activities = [activity.model_dump() for activity in engine.activities]
    conflicts_raw = detect_overlaps(activities)
    intent_collisions = analyze_intent_collisions(activities)
    for collision in intent_collisions:
        if "developer_ids" not in collision:
            collision["developer_ids"] = []
        collision["file_name"] = collision.get("module", "unknown")
        conflicts_raw.append(collision)

    conflicts = [
        ConflictDetail(
            developer_ids=conflict["developer_ids"],
            file_name=conflict["file_name"],
            overlap_type=conflict["overlap_type"],
            overlap_range=conflict.get("overlap_range", "module"),
            severity=conflict.get("severity", "MEDIUM"),
            reason_tags=conflict.get("reason_tags", []),
            module=conflict.get("module", "root"),
        )
        for conflict in conflicts_raw
    ]

    risk_summary = compute_risk_summary(activities)
    predictions = predict_future_conflicts(activities)
    explanation = build_explanations(conflicts_raw, predictions)
    return AnalysisResponse(
        conflicts=conflicts,
        risk=risk_summary,
        explanation=explanation,
        predictions=predictions,
    )


@app.get("/recommend")
def recommend() -> List[RecommendationItem]:
    activities = [activity.model_dump() for activity in engine.activities]
    recommendations = build_recommendations(activities)
    return [RecommendationItem(**recommendation) for recommendation in recommendations]


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("WebSocket connection accepted")
    while True:
        try:
            activities = [activity.model_dump(mode="json") for activity in engine.activities]

            if not activities:
                activities = [
                    {
                        "developer_id": "Dev1",
                        "file_name": "auth.py",
                        "start_line": 1,
                        "end_line": 1,
                        "timestamp": datetime.utcnow().isoformat() + "Z",
                        "additions": 0,
                        "deletions": 0,
                        "commit_message": "heartbeat",
                    }
                ]

            conflicts_raw = detect_overlaps(activities)
            intent_collisions = analyze_intent_collisions(activities)
            for collision in intent_collisions:
                if "developer_ids" not in collision:
                    collision["developer_ids"] = []
                collision["file_name"] = collision.get("module", "unknown")
                conflicts_raw.append(collision)

            risk_summary = compute_risk_summary(activities)
            recommendations = build_recommendations(activities)

            data = {
                "activity": activities,
                "overlap": conflicts_raw,
                "risk": risk_summary.model_dump(mode="json"),
                "decision": [RecommendationItem(**rec).model_dump(mode="json") for rec in recommendations],
            }

            state = engine.get_live_state()
            data.update(state)

            print("Sending:", data)

            await websocket.send_json(jsonable_encoder(data))
            await asyncio.sleep(2)

        except (WebSocketDisconnect, ConnectionClosedOK) as e:
            print("WebSocket closed by client:", e)
            break
        except Exception as e:
            print("WebSocket error:", e)
            await asyncio.sleep(2)
