export interface USSLatestItem {
  kelurahan_id: string;
  nama: string;
  uss: number;
  uss_level: string;
  climate_score: number;
  infrastructure_score: number;
  socioeconomic_score: number;
  computed_at: string;
}

export interface USSLatestResponse {
  data: USSLatestItem[];
  total: number;
  computed_at: string | null;
}

export interface USSHistoryItem {
  uss: number;
  climate_score: number;
  infrastructure_score: number;
  socioeconomic_score: number;
  uss_level: string;
  computed_at: string;
}

export interface ProjectionPoint {
  month: number;
  uss: number;
}

export interface ScenarioResponse {
  kelurahan_id: string;
  nama: string;
  current_uss: number;
  baseline_projection: ProjectionPoint[];
  intervention_projection: ProjectionPoint[];
  estimated_reduction: number;
}
