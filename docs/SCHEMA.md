# Database Schema — SIGAP

**Database**: PostgreSQL 15 + PostGIS 3.x

---

## Tabel Utama

### `users`
| Kolom | Tipe | Keterangan |
|-------|------|------------|
| id | UUID PK | |
| email | VARCHAR(255) UNIQUE | |
| hashed_password | VARCHAR(255) | bcrypt |
| full_name | VARCHAR(255) | |
| role | ENUM('admin','analyst','viewer') | |
| is_active | BOOLEAN DEFAULT true | |
| created_at | TIMESTAMP | |
| updated_at | TIMESTAMP | |

---

### `kelurahan`
| Kolom | Tipe | Keterangan |
|-------|------|------------|
| id | UUID PK | |
| kode_bps | VARCHAR(20) UNIQUE | Kode wilayah BPS |
| nama | VARCHAR(255) | |
| kecamatan | VARCHAR(255) | |
| kota | VARCHAR(255) | |
| provinsi | VARCHAR(255) | |
| geometry | GEOMETRY(MULTIPOLYGON,4326) | PostGIS boundary |
| centroid | GEOMETRY(POINT,4326) | PostGIS centroid |
| luas_km2 | NUMERIC(10,4) | |
| populasi | INTEGER | |
| created_at | TIMESTAMP | |

**Index**: `GIST(geometry)`, `GIST(centroid)`, `idx_kelurahan_kota`

---

### `indicators`
| Kolom | Tipe | Keterangan |
|-------|------|------------|
| id | UUID PK | |
| kelurahan_id | UUID FK → kelurahan | |
| dimension | ENUM('climate','infrastructure','socioeconomic') | |
| indicator_key | VARCHAR(100) | contoh: `rainfall_intensity` |
| value | NUMERIC(15,6) | Nilai raw |
| unit | VARCHAR(50) | contoh: `mm/jam` |
| source | VARCHAR(100) | contoh: `BMKG` |
| recorded_at | TIMESTAMP | Waktu data direkam dari sumber |
| ingested_at | TIMESTAMP DEFAULT NOW() | |

**Index**: `idx_indicators_kelurahan_dimension`, `idx_indicators_recorded_at`

---

### `uss_scores`
| Kolom | Tipe | Keterangan |
|-------|------|------------|
| id | UUID PK | |
| kelurahan_id | UUID FK → kelurahan | |
| uss | NUMERIC(5,2) | 0.00–100.00 |
| climate_score | NUMERIC(5,2) | |
| infrastructure_score | NUMERIC(5,2) | |
| socioeconomic_score | NUMERIC(5,2) | |
| uss_level | ENUM('very_low','low','medium','high','very_high') | |
| model_version | VARCHAR(50) | contoh: `v1.2.0` |
| computed_at | TIMESTAMP | |

**Index**: `idx_uss_kelurahan_computed_at`, `idx_uss_level`

---

### `alerts`
| Kolom | Tipe | Keterangan |
|-------|------|------------|
| id | UUID PK | |
| kelurahan_id | UUID FK → kelurahan | |
| uss_score_id | UUID FK → uss_scores | |
| trigger_level | ENUM('watch','warning','emergency') | |
| uss_value | NUMERIC(5,2) | USS saat trigger |
| message | TEXT | Pesan alert |
| is_resolved | BOOLEAN DEFAULT false | |
| resolved_at | TIMESTAMP NULLABLE | |
| created_at | TIMESTAMP | |

---

### `cascade_events`
| Kolom | Tipe | Keterangan |
|-------|------|------------|
| id | UUID PK | |
| kelurahan_id | UUID FK → kelurahan | |
| trigger_dimension | ENUM | Dimensi pemicu |
| affected_dimensions | JSONB | Array dimensi terdampak |
| correlation_score | NUMERIC(5,4) | Korelasi 0–1 |
| event_description | TEXT | |
| detected_at | TIMESTAMP | |

---

## Relasi
kelurahan (1) ──────── (N) indicators
kelurahan (1) ──────── (N) uss_scores
kelurahan (1) ──────── (N) alerts
kelurahan (1) ──────── (N) cascade_events
uss_scores (1) ───────(N) alerts