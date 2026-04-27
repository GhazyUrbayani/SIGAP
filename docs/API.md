# API Reference — SIGAP

**Base URL**: `http://localhost:8000/api/v1`  
**Auth**: Bearer JWT di header `Authorization: Bearer <token>`

---

## Authentication

### `POST /auth/login`
Login dan dapat JWT token.

**Request**:
```json
{
  "email": "admin@sigap.id",
  "password": "Admin123!"
}
```
**Response 200**:
```json
{
  "access_token": "eyJ...",
  "token_type": "bearer",
  "expires_in": 86400
}
```

---

## USS

### `GET /uss/latest`
Ambil USS terbaru semua kelurahan (dari Redis cache).

**Query Params**: `kota` (string, required)

**Response**:
```json
{
  "data": [
    {
      "kelurahan_id": "uuid",
      "nama": "Coblong",
      "uss": 72.4,
      "uss_level": "high",
      "climate_score": 68.1,
      "infrastructure_score": 75.3,
      "socioeconomic_score": 73.8,
      "computed_at": "2026-04-27T10:00:00Z"
    }
  ],
  "total": 151,
  "computed_at": "2026-04-27T10:00:00Z"
}
```

---

### `GET /uss/{kelurahan_id}/history`
Riwayat USS sebuah kelurahan.

**Query Params**: `from_date`, `to_date`, `limit` (default 30)

---

### `POST /uss/simulate`
Simulasi USS dengan indikator yang dimodifikasi.

**Request**:
```json
{
  "kelurahan_id": "uuid",
  "overrides": {
    "climate": { "rainfall_intensity": 120.0 },
    "infrastructure": { "road_damage_ratio": 0.4 }
  }
}
```
**Response**:
```json
{
  "original_uss": 72.4,
  "simulated_uss": 85.1,
  "delta": 12.7,
  "breakdown": { ... }
}
```

---

## Kelurahan

### `GET /kelurahan`
List kelurahan dengan USS terbaru.

**Query Params**: `kota`, `kecamatan`, `level`, `page`, `limit`

---

### `GET /kelurahan/{id}`
Detail satu kelurahan beserta USS, indikator, dan riwayat alert.

---

### `GET /kelurahan/geojson`
GeoJSON semua kelurahan dengan USS untuk Leaflet layer.

---

## Alerts

### `GET /alerts`
List alert aktif.

**Query Params**: `kota`, `level`, `is_resolved`, `from_date`, `to_date`

---

### `PATCH /alerts/{id}/resolve`
Tandai alert sebagai resolved.

---

## Reports

### `POST /reports/generate`
Generate laporan PDF/CSV.

**Request**:
```json
{
  "kota": "Bandung",
  "format": "pdf",
  "from_date": "2026-04-01",
  "to_date": "2026-04-27",
  "include_map": true
}
```
**Response**: Binary file atau signed URL download.