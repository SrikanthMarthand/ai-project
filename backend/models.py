from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class DeveloperActivity(BaseModel):
    developer_id: str = Field(..., description="Unique developer identifier")
    file_name: str = Field(..., description="Repository file path being edited")
    start_line: int = Field(..., ge=1, description="First line in the edit range")
    end_line: int = Field(..., ge=1, description="Last line in the edit range")
    timestamp: datetime = Field(..., description="UTC timestamp of the activity")
    additions: int = Field(0, ge=0, description="Number of added lines")
    deletions: int = Field(0, ge=0, description="Number of deleted lines")
    commit_message: Optional[str] = Field(None, description="Associated commit message or intent note")


class ConflictSeverity(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class ConflictDetail(BaseModel):
    developer_ids: List[str]
    file_name: str
    overlap_type: str
    overlap_range: str
    severity: ConflictSeverity
    reason_tags: List[str]
    module: str


class RiskSummary(BaseModel):
    probability: float
    level: ConflictSeverity
    score_components: dict


class AnalysisResponse(BaseModel):
    conflicts: List[ConflictDetail]
    risk: RiskSummary
    explanation: List[str]
    predictions: List[dict]


class RecommendationItem(BaseModel):
    action: str
    detail: str
    priority: str


class HotspotFile(BaseModel):
    file_name: str
    activity_count: int


class DeveloperCollision(BaseModel):
    developers: List[str]
    risk_count: int


class RiskTrendItem(BaseModel):
    timestamp: datetime
    risk_level: str
    score: float


class SimulationState(BaseModel):
    active_developers: List[str]
    active_files: List[str]
    hotspot_files: List[HotspotFile]
    developer_collisions: List[DeveloperCollision]
    health_score: float
    risk_trend: List[RiskTrendItem]
    last_updated: datetime
