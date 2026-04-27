# System Design — SIGAP

## 1. Struktur Folder
```
sigap/
├── README.md
├── docker-compose.dev.yml
├── ecosystem.config.js # PM2 config
├── .gitignore
│
├── docs/
│ ├── PRD.md
│ ├── SYSTEM_DESIGN.md # File ini
│ ├── SCHEMA.md
│ ├── API.md
│ ├── CONVENTIONS.md
│ ├── PLAN.md
│ ├── UIUX.md
│ └── PROMPTS.md
│
├── backend/
│ ├── .env.example
│ ├── requirements.txt
│ ├── requirements-dev.txt
│ ├── alembic.ini
│ ├── alembic/
│ │ └── versions/
│ ├── scripts/
│ │ ├── seed_kelurahan.py
│ │ ├── seed_dummy_indicators.py
│ │ └── run_initial_uss.py
│ ├── tests/
│ │ ├── conftest.py
│ │ ├── test_uss_engine.py
│ │ ├── test_auth.py
│ │ └── test_alerts.py
│ └── app/
│ ├── main.py # FastAPI entry point
│ ├── config.py # Settings via pydantic-settings
│ ├── database.py # DB session factory
│ ├── dependencies.py # Shared FastAPI dependencies
│ │
│ ├── models/ # SQLAlchemy ORM models
│ │ ├── _init_.py
│ │ ├── kelurahan.py
│ │ ├── indicator.py
│ │ ├── uss_score.py
│ │ ├── alert.py
│ │ └── user.py
│ │
│ ├── schemas/ # Pydantic request/response schemas
│ │ ├── _init_.py
│ │ ├── kelurahan.py
│ │ ├── uss.py
│ │ ├── alert.py
│ │ └── auth.py
│ │
│ ├── api/
│ │ └── v1/
│ │ ├── router.py # Aggregate semua routers
│ │ ├── auth.py
│ │ ├── kelurahan.py
│ │ ├── uss.py
│ │ ├── alerts.py
│ │ ├── simulator.py
│ │ └── reports.py
│ │
│ ├── services/ # Business logic layer
│ │ ├── uss_engine.py # Kalkulasi USS
│ │ ├── cascade_model.py # Cascading failure detection
│ │ ├── alert_engine.py # Trigger & notif logic
│ │ ├── data_ingestion.py# Fetch dari BMKG, BPS, OSM
│ │ └── ai_advisor.py # Azure OpenAI integration
│ │
│ ├── ml/
│ │ ├── train.py # Training script
│ │ ├── predict.py # Inference
│ │ └── models/ # Saved .pkl files
│ │ └── uss_model_v1.pkl
│ │
│ └── tasks/
│ └── scheduler.py # APScheduler cron jobs
│
└── frontend/
├── .env.example
├── package.json
├── tsconfig.json
├── vite.config.ts
├── tailwind.config.ts
├── index.html
└── src/
├── main.tsx
├── App.tsx
├── router.tsx # React Router config
│
├── types/ # Global TypeScript interfaces
│ ├── uss.ts
│ ├── kelurahan.ts
│ └── auth.ts
│
├── lib/
│ ├── api.ts # Axios instance + interceptors
│ └── utils.ts
│
├── hooks/ # Custom React hooks
│ ├── useUSS.ts
│ ├── useAlerts.ts
│ └── useAuth.ts
│
├── store/ # Zustand global state
│ ├── authStore.ts
│ └── mapStore.ts
│
├── components/
│ ├── ui/ # Generic reusable components
│ │ ├── Button.tsx
│ │ ├── Badge.tsx
│ │ ├── Card.tsx
│ │ └── Skeleton.tsx
│ ├── map/
│ │ ├── ChoroplethMap.tsx
│ │ ├── KelurahanLayer.tsx
│ │ └── MapLegend.tsx
│ ├── dashboard/
│ │ ├── USSCard.tsx
│ │ ├── AlertPanel.tsx
│ │ ├── TrendChart.tsx
│ │ └── DimensionBreakdown.tsx
│ └── layout/
│ ├── Sidebar.tsx
│ ├── Header.tsx
│ └── PageLayout.tsx
│
└── pages/
├── Login.tsx
├── Dashboard.tsx
├── KelurahanDetail.tsx
├── Simulator.tsx
├── Alerts.tsx
└── Reports.tsx

```

## 2. Data Flow
Scheduler (tiap jam)
└─► DataIngestionService.fetch_all()
├─► BMKG API → tabel indicator (dimensi: climate)
├─► BPS API → tabel indicator (dimensi: socioeconomic)
└─► OSM API → tabel indicator (dimensi: infrastructure)

Setelah ingest selesai:
└─► USSEngine.compute_all_kelurahan()
├─► Load indikator dari DB
├─► Normalize 0–1
├─► XGBoost predict → raw_score
└─► Simpan ke tabel uss_score + cache ke Redis

AlertEngine.check_thresholds()
└─► Bandingkan USS terbaru vs threshold
└─► Jika terlampaui → buat record alert + kirim notifikasi

Frontend polling setiap 60 detik
└─► GET /api/v1/uss/latest → ambil dari Redis cache

text

## 3. Authentication Flow
POST /auth/login
├─► Validasi credentials
├─► Generate access_token (JWT, 24h) + refresh_token (7d)
└─► Return tokens

Protected routes → Bearer token di header Authorization
└─► JWTBearer dependency decode & verify
└─► Inject current_user ke route handler