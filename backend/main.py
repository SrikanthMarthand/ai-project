from datetime import datetime
import asyncio

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.encoders import jsonable_encoder
from websockets.exceptions import ConnectionClosedOK

# 🔥 ENGINE IMPORTS
from backend.engine.github_fetch import fetch_commits
from backend.engine.github_parser import parse_commits
from backend.engine.overlap import detect_overlaps
from backend.engine.intent import analyze_intent_collisions
from backend.engine.risk import compute_risk_summary
from backend.engine.decision import build_recommendations
from backend.models import RecommendationItem
from backend.engine.github_details import get_commit_details
from dotenv import load_dotenv
load_dotenv()
latest_activity = []
repo_config = {
    "owner": "facebook",
    "repo": "react"
}
app = FastAPI()

# ✅ TEST ROUTE
@app.get("/")
def home():
    return {"msg": "Backend running"}
from fastapi import Request

@app.post("/webhook")
async def github_webhook(request: Request):
    global latest_activity

    payload = await request.json()

    print("📡 Webhook received")

    if "commits" in payload:
        commits = payload["commits"]

        activities = []

        for c in commits:
            activities.append({
                "developer_id": c["author"]["name"],
                "file_name": c["modified"][0] if c.get("modified") else "unknown",
                "start_line": 1,
                "end_line": 20,
                "timestamp": c["timestamp"],
                "additions": 0,
                "deletions": 0,
                "commit_message": c["message"]
            })

        latest_activity = activities

        print("✅ Updated latest_activity:", latest_activity)

    return {"status": "received"}
# ✅ WEBSOCKET
from fastapi import Request

@app.post("/webhook")
async def github_webhook(request: Request):
    global latest_activity

    payload = await request.json()

    print("📡 Webhook received")

    owner = repo_config["owner"]
    repo = repo_config["repo"]

    if "commits" in payload:
        commits = payload["commits"]

        activities = []

        for c in commits:
            developer = c["author"]["name"]
            sha = c["id"]

            # 🔥 GET REAL FILE DETAILS FROM GITHUB API
            files = get_commit_details(owner, repo, sha)

            if not files:
                # fallback
                activities.append({
                    "developer_id": developer,
                    "file_name": "unknown",
                    "start_line": 1,
                    "end_line": 20,
                    "timestamp": c["timestamp"],
                    "additions": 0,
                    "deletions": 0,
                    "commit_message": c["message"]
                })
            else:
                # 🔥 REAL DATA LOOP
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

        print("✅ Updated latest_activity with REAL GitHub data:", latest_activity)

    return {"status": "received"}