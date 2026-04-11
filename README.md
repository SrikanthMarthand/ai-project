# DevTwin AI

DevTwin AI is a full-stack repository intelligence platform built to prevent merge conflicts before they happen. It combines real-time simulation, intent extraction, overlap detection, risk scoring, future conflict forecasting, causal explanation, and decision recommendations.

## Architecture

- `backend/` - FastAPI service powering repository simulation and intelligence engines
- `frontend/` - React dashboard for live activity, conflict intelligence, AI insights, and recommendations

## Backend Structure

- `backend/main.py` - FastAPI API endpoints
- `backend/models.py` - Pydantic request/response models
- `backend/engine/` - Modular conflict detection engines
  - `simulation.py` - live developer activity simulation
  - `overlap.py` - line-level and file-level overlap detection
  - `intent.py` - intent extraction and module collision detection
  - `risk.py` - risk score computation
  - `simulation_future.py` - future conflict prediction
  - `explain.py` - human-readable explanation generation
  - `decision.py` - actionable recommendation engine

## Frontend Structure

- `frontend/src/App.tsx` - dashboard orchestration and polling
- `frontend/src/components/` - UI panels for activity, conflict, insights, and decisions
- `frontend/src/hooks/usePolling.ts` - reusable polling hook
- `frontend/src/styles.css` - dark theme SaaS dashboard styling

## Setup and Run

### Backend

1. Create a Python virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install backend dependencies

```powershell
pip install -r backend/requirements.txt
```

3. Run the API

```powershell
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend

1. Install dependencies

```powershell
cd frontend
npm install
```

2. Start development server

```powershell
npm run dev
```

3. Open the dashboard at `http://localhost:5173`

## API Endpoints

- `POST /simulate` - add or update developer activity
- `GET /state` - retrieve current live repository state
- `POST /analyze` - analyze conflicts, risk, and predictions
- `GET /recommend` - fetch decision recommendations

### Example payload

```json
{
  "developer_id": "dev-anna",
  "file_name": "src/auth/login.ts",
  "start_line": 14,
  "end_line": 28,
  "timestamp": "2026-04-07T12:34:56Z",
  "additions": 12,
  "deletions": 4,
  "commit_message": "Improve login auth flow and token refresh"
}
```

## Notes

- The frontend uses polling to simulate real-time updates.
- The system is designed for extensibility and can be wired into source control events, branch metadata, and CI systems.
