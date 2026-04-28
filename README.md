# SIGAP (Sistem Intelijen Geospasial Ancaman Perkotaan)

**Smart Integrated Geo-Analytics for Urban Pressure**

> Dashboard analitik kerentanan urban berbasis ML untuk Pemerintah Daerah Indonesia.
> Menghitung Urban Stress Score (USS) per kelurahan, mendeteksi cascading failure,
> dan menghasilkan alert serta rekomendasi tindakan yang actionable.

---

## 🎯 Features

- **Urban Stress Score (USS) Engine** — ML-powered scoring (0–100) per kelurahan
  combining climate, infrastructure, and socioeconomic indicators
- **Choropleth Map** — Interactive zone-colored map (GREEN/YELLOW/RED) with drill-down
- **Cascading Failure Detection** — Non-linear interaction modeling across dimensions
- **Dynamic Trigger System** — Automated BMKG data ingestion every 6 hours with
  anomaly detection (z-score > 2σ)
- **Alert Engine** — Rule-based NLG generating actionable alerts in Bahasa Indonesia
- **Scenario Simulator** — What-if analysis projecting USS over 12/24/36/60 months
- **JWT Authentication** — Role-based access (Admin, Analyst, Viewer)

---

## 🏗️ Tech Stack

| Layer     | Technology                                          |
| --------- | --------------------------------------------------- |
| Backend   | FastAPI · Python 3.11 · PostgreSQL 15 + PostGIS · Redis |
| Frontend  | React 18 · TypeScript · Tailwind CSS · Vite         |
| ML        | scikit-learn · XGBoost · LightGBM · Isolation Forest|
| Maps      | Azure Maps (SVG prototype for local dev)            |
| Auth      | JWT (access + refresh tokens)                       |
| DevOps    | Docker · docker-compose                             |

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

- **Frontend**: https://purple-pebble-0fa7c9700.7.azurestaticapps.net/ | https://sigap-frontend.onrender.com/
- **Backend API**: sigap-api-lvynv3vb42tuc.azurewebsites.net | https://sigap-backend-61rh.onrender.com

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

The Urban Stress Score is computed using a multi-dimensional weighted model:

```
USS = base_score × (1 + interaction_multiplier)

where:
  base_score = 0.40 × Climate + 0.35 × Infrastructure + 0.25 × SocioEconomic
  interaction_multiplier = cascading_failure_factor(Climate, Infra, SocEco)
```

- **Climate indicators**: rainfall intensity, flood frequency, temperature anomaly, humidity
- **Infrastructure indicators**: road damage ratio, drainage quality, building density, green space
- **Socioeconomic indicators**: poverty rate, unemployment, health facility access, education index

Cascading failure uses a non-linear geometric mean approach to model compounding effects.

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
