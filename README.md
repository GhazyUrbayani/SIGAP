# SIGAP (Sistem Intelijen Geospasial Ancaman Perkotaan)

**Smart Integrated Geo-Analytics for Urban Pressure**

> Dashboard analitik kerentanan urban berbasis ML untuk Pemerintah Daerah Indonesia.
> Menghitung Urban Stress Score (USS) per kelurahan, mendeteksi cascading failure,
> dan menghasilkan alert serta rekomendasi tindakan yang actionable.

---

## 🎯 Features

- **Urban Stress Score (USS) Engine** — Model Ensemble (XGBoost / LightGBM / Random Forest — dibandingkan, dipilih terbaik via RMSE/AUC) + Isolation Forest untuk validasi anomali. Skor kerentanan 0–100 per kelurahan berdasarkan 3 dimensi: Iklim, Infrastruktur, dan Sosial-Ekonomi.
- **Cascading Failure Modeler** — Mendeteksi interaksi antar-dimensi dengan interaction term non-linear. Skor melonjak jika ≥2 dimensi kritis bersamaan (banjir tinggi × infrastruktur buruk × kemiskinan tinggi = efek domino).
- **Dynamic Trigger System** — Pipeline otomatis menarik data BMKG per minggu, deteksi anomali via z-score > 2σ, dan memicu pembaruan USS jika threshold terlampaui.
- **Choropleth Dashboard** — Visualisasi HeatMap interaktif dengan zona 🟢 HIJAU / 🟡 KUNING / 🔴 MERAH, dilengkapi drill-down per RT/RW dan grafik tren historis USS ≥30 hari.
- **Actionable Alert Engine** — Generator rekomendasi teks natural language Bahasa Indonesia per kelurahan zona KUNING/MERAH. Menampilkan penyebab, lokasi titik kritis, dan tenggat aksi.
- **Skenario Simulator** — Fitur "bagaimana jika" untuk perencana kota: simulasi dampak pembangunan infrastruktur terhadap USS 5 tahun ke depan, dengan tampilan baseline vs intervensi.
- **JWT Authentication** — Role-based access (Admin, Analyst, Viewer)

---

## 🏗️ Tech Stack

| Layer     | Technology                                          |
| --------- | --------------------------------------------------- |
| Backend   | FastAPI · Python 3.11 · PostgreSQL 15 + PostGIS · Redis |
| Frontend  | React 18 · TypeScript · Tailwind CSS · Vite         |
| ML        | scikit-learn · XGBoost · LightGBM · Isolation Forest |
| Maps      | Azure Maps (SVG prototype for local dev)            |
| Auth      | JWT (access + refresh tokens)                       |
| DevOps    | Docker · docker-compose                             |

### Azure Cloud Services

| Service | Fungsi |
|---------|--------|
| **Azure Machine Learning** | Training, deployment, dan monitoring model anomaly detection (Isolation Forest) + ensemble classifier (XGBoost / LightGBM) |
| **Azure Event Hubs** | Ingest stream data BMKG real-time (curah hujan, suhu, kelembaban) |
| **Azure Maps** | Visualisasi choropleth dinamis — HeatMap layer-ed overlay multi-hazard |
| **Azure Synapse Analytics** | Pipeline ETL integrator data BMKG, BPS, OSM, dan PUPR |
| **Power BI Embedded** | Dashboard eksekutif untuk stakeholder (tanpa instalasi) |

### Dataset Open Source

| Sumber | Deskripsi |
|--------|-----------|
| **BMKG Open Data API** | Data iklim (curah hujan, suhu, kelembaban) |
| **BPS Statistik Kemiskinan 2023–2024** | Indikator sosial-ekonomi per wilayah |
| **OpenStreetMap Indonesia** | Kondisi jalan & drainase |
| **BNPB GIS Disaster History** | Histori kejadian bencana |
| **Riskesdas** | Indeks kesehatan per kelurahan |

---

## 📋 Prerequisites

- **Docker** ≥ 20.x & Docker Compose ≥ 2.x
- **Node.js** ≥ 20.x (for frontend development)
- **Python** ≥ 3.11 (for local backend development without Docker)

---

## 🚀 Quick Start

### 1. Clone & Configure

```bash
git clone https://github.com/GhazyUrbayani/SIGAP.git
cd sigap
cp .env.example .env
```

### 2. Start All Services

```bash
make dev
```

This starts PostgreSQL + PostGIS, Redis, Backend (FastAPI), and Frontend (Vite).

### 3. Run Migrations & Seed Data

```bash
make migrate
make seed
```

### 4. Open the App

- **Frontend**: [http://localhost:5173](http://localhost:5173)
- **Backend API**: [http://localhost:8000](http://localhost:8000)
- **API Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)

### 5. Login Credentials

| Role    | Email              | Password    |
| ------- | ------------------ | ----------- |
| Admin   | admin@sigap.id     | Admin123!   |
| Analyst | analyst@sigap.id   | Analyst123! |
| Viewer  | viewer@sigap.id    | Viewer123!  |

---

## 🧪 Running Tests

```bash
make test
```

Or run individually:

```bash
# Backend tests
docker-compose exec backend pytest tests/ -v

# Frontend tests (requires npm install first)
cd frontend && npm test -- --run
```

---

## 📁 Project Structure

```
sigap/
├── docs/                  # Product docs (PRD, API, Schema, etc.)
├── backend/
│   ├── app/
│   │   ├── main.py        # FastAPI entry point
│   │   ├── config.py      # Settings (pydantic-settings)
│   │   ├── database.py    # Async SQLAlchemy + PostGIS
│   │   ├── models/        # ORM models
│   │   ├── schemas/       # Pydantic request/response
│   │   ├── api/v1/        # Route handlers
│   │   ├── services/      # Business logic (USS Engine, Alert Engine)
│   │   ├── ml/            # ML training & inference
│   │   └── tasks/         # APScheduler cron jobs
│   ├── alembic/           # Database migrations
│   ├── scripts/           # Seed data scripts
│   └── tests/             # pytest test suite
├── frontend/
│   └── src/
│       ├── components/    # React components (map, dashboard, layout)
│       ├── pages/         # Page components (Login, Dashboard, Alerts, Simulator)
│       ├── hooks/         # Custom React hooks
│       ├── store/         # Zustand state management
│       ├── lib/           # API client, utilities
│       └── types/         # TypeScript interfaces
├── docker-compose.yml
├── Makefile
└── .env.example
```

---

## 🏙️ USS Engine Details

The Urban Stress Score is computed using a **model ensemble** approach with **non-linear interaction terms**:

```
USS = base_score × (1 + interaction_multiplier)

where:
  base_score = w₁ × Climate + w₂ × Infrastructure + w₃ × SocioEconomic
  interaction_multiplier = cascading_failure_factor(Climate, Infra, SocEco)

  Bobot (w) dikalibrasi menggunakan model terpilih terhadap data historis
  kejadian bencana BPBD.
```

**Model Comparison**: XGBoost, LightGBM, dan Random Forest dibandingkan — model terbaik dipilih berdasarkan evaluasi RMSE/AUC. Isolation Forest digunakan sebagai **validasi anomali** untuk memastikan skor USS tidak mengandung outlier yang tidak terdeteksi.

**Dimensi USS**:
- **Climate**: rainfall intensity, flood frequency, temperature anomaly, humidity
- **Infrastructure**: road damage ratio, drainage quality, building density, green space
- **Socioeconomic**: poverty rate, unemployment, health facility access, education index

**Cascading Failure**: Menggunakan non-linear geometric mean approach. Skor melonjak jika ≥2 dimensi kritis bersamaan (banjir tinggi × infrastruktur buruk × kemiskinan tinggi = efek domino non-linear). Feature Importance per interaction term tersedia untuk transparansi model.

**Zona USS**:
- 🟢 **Hijau (USS 0–39)**: Aman, tidak ada aksi darurat
- 🟡 **Kuning (USS 40–69)**: Waspada, rekomendasikan inspeksi rutin
- 🔴 **Merah (USS 70–100)**: Darurat, aksi segera diperlukan

---

## 🔔 Alert Engine

Setiap kelurahan zona KUNING/MERAH dilengkapi rekomendasi teks **natural language** Bahasa Indonesia yang menampilkan penyebab, lokasi titik kritis, dan tenggat aksi.

**Contoh Output**:
> *"Kelurahan X masuk ZONA MERAH karena anomali curah hujan +340% dari baseline, 3 titik drainase kritis teridentifikasi di RW 05, 09, 14 dan sekitarnya. Rekomendasi: inspeksi fisik dan siagakan tim BPBD dalam 48 jam."*

**Trigger Levels**:

| Level | USS Range | Aksi |
|-------|-----------|------|
| **Watch** | 60–69 | Notifikasi email ke Analyst |
| **Warning** | 70–79 | Notifikasi email + in-app ke BPBD |
| **Emergency** | ≥80 | Push notification + laporan otomatis ke Kepala Daerah |

---

## 🧑‍💼 Cara Penggunaan (User Flow)

### Flow Pengguna (Petugas Pemda / BPBD)

**Langkah 1 — Login Dashboard**
Pengguna mengakses portal SIGAP melalui **browser**. Login menggunakan akun Pemda (integrasi SSO atau credential demo). **Tidak diperlukan instalasi software tambahan.**

**Langkah 2 — Lihat Peta Urban Stress Score**
Halaman utama menampilkan peta kota dengan warna per kelurahan:
- 🟢 **Hijau (USS 0–39)**: Aman, tidak ada aksi darurat
- 🟡 **Kuning (USS 40–69)**: Waspada, rekomendasikan inspeksi rutin
- 🔴 **Merah (USS 70–100)**: Darurat, aksi segera diperlukan

**Langkah 3 — Drill-down Kelurahan**
Klik satu kelurahan → tampil panel detail:
- Skor tiap dimensi (Iklim / Infrastruktur / Sosial-Ekonomi)
- Grafik tren USS 30 hari terakhir
- Peta titik-titik infrastruktur kritis

**Langkah 4 — Baca Rekomendasi Aksi**
Setiap kelurahan zona KUNING/MERAH dilengkapi **teks rekomendasi spesifik**, ditampilkan dalam Bahasa Indonesia yang dapat langsung dipahami aparatur **tanpa keahlian teknis**.

**Langkah 5 — Jalankan Simulasi**
Petugas perencana dapat menggunakan fitur **simulator** untuk melihat proyeksi USS jika infrastruktur di titik tertentu diperbaiki atau anggaran dialihkan. Tampilan perbandingan baseline vs intervensi tersedia untuk evaluasi kebijakan.

---

## ☁️ Deployment

### 🟢 Option A — Render (Free, Fast for Dev/Testing)

The repo includes `render.yaml` — just connect your GitHub repo:

```bash
1. Go to https://render.com → Sign up with GitHub
2. Click "New" → "Blueprint"
3. Select your SIGAP repo
4. Render reads render.yaml → deploys everything automatically
5. Wait ~5-10 minutes for first build
```

After deploy, run migrations via Render Shell:
```bash
# In Render Dashboard → sigap-backend → Shell:
alembic upgrade head
python -m scripts.seed_kelurahan
python -m scripts.seed_dummy_indicators
python -m scripts.run_initial_uss
```

### 🔵 Option B — Azure (For Competition Demo — Required)

```bash
# Install Azure Developer CLI
brew tap azure/azd && brew install azd

# Login & Init
az login
azd auth login
azd init    # Environment: sigap-prod, Location: Southeast Asia

# Deploy everything
azd up      # ~15-20 minutes

# Set env vars
azd env set BMKG_API_URL "https://data.bmkg.go.id/api/"
azd env set JWT_SECRET_KEY "$(openssl rand -hex 32)"
azd deploy  # redeploy with new env
```

### Deployment Comparison

| | Render (Free) | Azure (Free 12mo) |
|---|---|---|
| **Setup** | ~15 min | ~30 min |
| **Cold start** | 30-60s ⚠️ | None ✅ |
| **PostGIS** | ✅ extension | ✅ native |
| **Competition score** | ❌ | ✅ Best Azure Tech = Rp2.5jt |
| **URL** | `.onrender.com` | `.azurewebsites.net` |

---

## 📝 License

MIT — Built for Pemerintah Kota Bandung urban resilience initiative.