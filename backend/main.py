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

# ✅ GLOBAL STATE
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


# 🔥 GITHUB WEBHOOK (FINAL FIXED VERSION)
@app.post("/webhook")
async def github_webhook(request: Request):
    global latest_activity

    payload = await request.json()
    print("📡 Webhook received")

    owner = repo_config["owner"]
    repo = repo_config["repo"]

    new_activities = []

    commits = payload.get("commits", [])

    if not commits:
        print("⚠️ No commits in payload")

    for c in commits:
        developer = c.get("author", {}).get("name", "unknown")
        sha = c.get("id")

        print(f"➡️ Processing commit by {developer} | sha: {sha}")

        files = get_commit_details(owner, repo, sha)

        # 🔥 FALLBACK if GitHub API fails
        if not files:
            print("⚠️ No file data from API, using fallback")
            files = [{
                "file_name": "unknown_file",
                "additions": 1,
                "deletions": 0
            }]

        for f in files:
            new_activities.append({
                "developer_id": developer,
                "file_name": f.get("file_name", "unknown"),
                "start_line": 1,
                "end_line": f.get("additions", 1) + f.get("deletions", 0) + 1,
                "timestamp": c.get("timestamp"),
                "additions": f.get("additions", 0),
                "deletions": f.get("deletions", 0),
                "commit_message": c.get("message")
            })

    # ✅ ACCUMULATE (MULTI DEV FIX)
    latest_activity.extend(new_activities)
    latest_activity = latest_activity[-50:]

    print("✅ REAL activity count:", len(latest_activity))
    print("👨‍💻 Developers:",
          list(set(a["developer_id"] for a in latest_activity)))

    return {"status": "received"}


# 🔥 WEBSOCKET (FINAL STABLE)
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("✅ WebSocket connected")

    try:
        while True:
            global latest_activity

            activities = latest_activity if latest_activity else []

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
                 #demo
            await websocket.send_json(jsonable_encoder(data))

            print("🚀 DATA SENT | devs:",
                  len(data["active_developers"]),
                  "| files:",
                  len(data["active_files"]))

            await asyncio.sleep(2)

    except WebSocketDisconnect:
        print("🔌 WebSocket disconnected")
 
    except Exception as e:
        print("❌ Error:", e)