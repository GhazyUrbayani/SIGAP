export interface User {
  id: string;
  email: string;
  full_name: string;
  role: string;
  is_active: boolean;
}

export interface TokenResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
  expires_in: number;
}

export interface AlertItem {
  id: string;
  kelurahan_id: string;
  kelurahan_nama: string | null;
  trigger_level: string;
  uss_value: number;
  message: string;
  is_resolved: boolean;
  resolved_at: string | null;
  created_at: string;
}

export interface AlertListResponse {
  data: AlertItem[];
  total: number;
}
