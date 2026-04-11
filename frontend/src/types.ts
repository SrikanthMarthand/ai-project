export interface DeveloperActivity {
  developer_id: string;
  file_name: string;
  start_line: number;
  end_line: number;
  timestamp: string;
  additions: number;
  deletions: number;
  commit_message?: string;
}

export interface ConflictDetail {
  developer_ids: string[];
  file_name: string;
  overlap_type: string;
  overlap_range: string;
  severity: string;
  reason_tags: string[];
  module: string;
}

export interface RiskSummary {
  probability: number;
  level: string;
  score_components: Record<string, number>;
}

export interface RecommendationItem {
  action: string;
  detail: string;
  priority: string;
}

export interface SimulationState {
  active_developers: string[];
  active_files: string[];
  hotspot_files: Array<{ file_name: string; activity_count: number }>;
  developer_collisions: Array<{ developers: string[]; risk_count: number; files: string[] }>;
  health_score: number;
  risk_trend: Array<{ window: number; risk: number }>;
  last_updated: string;
}
