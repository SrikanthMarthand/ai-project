from datetime import datetime
import asyncio

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

from backend.engine.overlap import detect_overlaps
from backend.engine.intent import analyze_intent_collisions
from backend.engine.risk import compute_risk_summary
from backend.engine.decision import build_recommendations
from backend.engine.github_details import get_commit_details
from backend.models import RecommendationItem

# ✅ GLOBAL STATE (REAL DATA ONLY)

latest_activity = []

repo_config = {
"owner": "SrikanthMarthand",
"repo": "ai-project"
}

app = FastAPI()

# ✅ CORS

app.add_middleware(
CORSMiddleware,
allow_origins=["*"],
allow_credentials=True,
allow_methods=["*"],
allow_headers=["*"],
)

# ✅ TEST ROUTE

@app.get("/")
def home():
    return {"msg": "Backend running 🚀"}

# 🔥 GITHUB WEBHOOK (REAL DATA ONLY)
 
@app.post("/webhook")
async def github_webhook(request: Request):
    global latest_activity

    payload = await request.json()
    print("Webhook received")

    owner = repo_config["owner"]
    repo = repo_config["repo"]

    activities = []

    if "commits" in payload:
        for c in payload["commits"]:
            developer = c["author"]["name"]
            sha = c["id"]

            files = get_commit_details(owner, repo, sha)

            if not files:
                continue

            for f in files:
                activities.append({
                    "developer_id": developer,
                    "file_name": f["file_name"],
                    "start_line": 1,
                    "end_line": f["additions"] + f["deletions"] + 1,
                    "timestamp": c["timestamp"],
                    "additions": f["additions"],
                    "deletions": f["deletions"],
                    "commit_message": c["message"]
                })

    latest_activity = activities
    print("REAL activity:", latest_activity)

    return {"status": "received"}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("WebSocket connected")

    try:
        while True:
            global latest_activity

            if not latest_activity:
                await asyncio.sleep(1)
                continue

            latest_activity.extend(activities)
            latest_activity = latest_activity[-50:]

            conflicts_raw = detect_overlaps(activities)

            intent_collisions = analyze_intent_collisions(activities)
            for c in intent_collisions:
                c["file_name"] = c.get("module", "unknown")
                conflicts_raw.append(c)

            risk_summary = compute_risk_summary(activities)
            recommendations = build_recommendations(activities)

            data = {
                "activity": activities,
                "overlap": conflicts_raw,
                "risk": risk_summary.model_dump(mode="json"),
                "decision": [
                    RecommendationItem(**rec).model_dump(mode="json")
                    for rec in recommendations
                ],
                "active_developers": list(set(a["developer_id"] for a in activities)),
                "active_files": list(set(a["file_name"] for a in activities)),
                "health_score": 85,
                "last_updated": datetime.utcnow().isoformat(),
            }

            await websocket.send_json(jsonable_encoder(data))
            print("DATA SENT")

            await asyncio.sleep(2)

    except WebSocketDisconnect:
        print("WebSocket disconnected")

    except Exception as e:
        print("Error:", e)
# demo change for aryan 1223