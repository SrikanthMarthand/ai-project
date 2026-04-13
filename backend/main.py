from datetime import datetime
import asyncio

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from websockets.exceptions import ConnectionClosedOK
from dotenv import load_dotenv

load_dotenv()

from backend.engine.overlap import detect_overlaps
from backend.engine.intent import analyze_intent_collisions
from backend.engine.risk import compute_risk_summary
from backend.engine.decision import build_recommendations
from backend.engine.github_details import get_commit_details
from backend.models import RecommendationItem

latest_activity = []

repo_config = {
    "owner": "SrikanthMarthand",
    "repo": "ai-project"
}

app = FastAPI()
# akbar change
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"msg": "Backend running 🚀"}


# 🔥 WEBHOOK
@app.post("/webhook")
async def github_webhook(request: Request):
    global latest_activity

    payload = await request.json()
    print("📡 Webhook received")

    owner = repo_config["owner"]
    repo = repo_config["repo"]

    activities = []

    if "commits" in payload:
        for c in payload["commits"]:
            developer = c["author"]["name"]
            sha = c["id"]

            files = get_commit_details(owner, repo, sha)

            for f in files:
                base = {
                    "developer_id": developer,
                    "file_name": f["file_name"],
                    "start_line": 1,
                    "end_line": f["additions"] + f["deletions"] + 1,
                    "timestamp": c["timestamp"],
                    "additions": f["additions"],
                    "deletions": f["deletions"],
                    "commit_message": c["message"]
                }

                activities.append(base)

                # 🔥 DEMO BOOST
                activities.append({
                    **base,
                    "developer_id": "dev-alex",
                    "start_line": 5,
                    "end_line": 25,
                    "commit_message": "Refactoring logic"
                })

                activities.append({
                    **base,
                    "developer_id": "dev-priya",
                    "start_line": 10,
                    "end_line": 30,
                    "commit_message": "Validation changes"
                })

                activities.append({
                    "developer_id": "dev-lee",
                    "file_name": "src/utils/helper.js",
                    "start_line": 1,
                    "end_line": 20,
                    "timestamp": c["timestamp"],
                    "additions": 6,
                    "deletions": 1,
                    "commit_message": "Utility update"
                })

    latest_activity = activities
    print("✅ Updated activity:", latest_activity)

    return {"status": "received"}


# 🔥 WEBSOCKET
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("✅ WebSocket connected")

    while True:
        try:
            global latest_activity

            # 🔥 FIXED (PROPERLY INSIDE LOOP)
            if latest_activity:
                activities = latest_activity
            else:
                print("🔥 USING DEMO DATA")

                activities = [
                    {
                        "developer_id": "dev-akash",
                        "file_name": "src/auth/login.js",
                        "start_line": 1,
                        "end_line": 20,
                        "timestamp": datetime.utcnow().isoformat(),
                        "additions": 12,
                        "deletions": 3,
                        "commit_message": "Login logic update"
                    },
                    {
                        "developer_id": "dev-priya",
                        "file_name": "src/auth/login.js",
                        "start_line": 10,
                        "end_line": 30,
                        "timestamp": datetime.utcnow().isoformat(),
                        "additions": 8,
                        "deletions": 2,
                        "commit_message": "Validation changes"
                    },
                    {
                        "developer_id": "dev-rahul",
                        "file_name": "src/utils/helper.js",
                        "start_line": 1,
                        "end_line": 15,
                        "timestamp": datetime.utcnow().isoformat(),
                        "additions": 5,
                        "deletions": 1,
                        "commit_message": "Helper optimization"
                    },
                    {
                        "developer_id": "dev-alex",
                        "file_name": "src/auth/login.js",
                        "start_line": 5,
                        "end_line": 25,
                        "timestamp": datetime.utcnow().isoformat(),
                        "additions": 6,
                        "deletions": 1,
                        "commit_message": "Refactor auth logic"
                    }
                ]

            # 🔥 ANALYSIS
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
            print("🚀 DATA SENT")

            await asyncio.sleep(2)

        except (WebSocketDisconnect, ConnectionClosedOK):
            print("❌ WebSocket disconnected")
            break

        except Exception as e:
            print("❌ Error:", e)
            await asyncio.sleep(2)