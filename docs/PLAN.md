# Development Plan — SIGAP

## Milestone Overview

| Fase | Scope | Target |
|------|-------|--------|
| **M0** | Setup & Fondasi | Hari 1–2 |
| **M1** | Data + USS Engine | Hari 3–5 |
| **M2** | Dashboard + Peta | Hari 6–8 |
| **M3** | Alert + Simulator | Hari 9–11 |
| **M4** | Polish + Demo Prep | Hari 12–14 |

---

## Checklist per Milestone

### M0 — Setup & Fondasi
- [ ] Inisialisasi repo, folder structure, README
- [ ] Docker Compose untuk PostgreSQL + Redis
- [ ] FastAPI boilerplate + config + health endpoint
- [ ] Alembic migrations untuk semua tabel
- [ ] React + TypeScript + Tailwind setup
- [ ] Auth system (login, JWT, RBAC)
- [ ] CI pipeline dasar (lint + test)

### M1 — Data & USS Engine
- [ ] Data ingestion service (BMKG, BPS mock)
- [ ] Seed data kelurahan Bandung (151 kelurahan)
- [ ] USS Engine v1 (weighted formula)
- [ ] ML model training script (XGBoost)
- [ ] Scheduler cron job (APScheduler)
- [ ] Endpoint `/uss/latest` dengan Redis cache

### M2 — Dashboard & Peta
- [ ] Choropleth map Leaflet + GeoJSON layer
- [ ] USS color coding 5 level
- [ ] Drill-down popup per kelurahan
- [ ] Trend chart (Recharts)
- [ ] Dimension breakdown chart
- [ ] Sidebar + Header layout

### M3 — Alert & Simulator
- [ ] Alert Engine (threshold check)
- [ ] Alert list UI + resolve action
- [ ] Cascading failure detection basic
- [ ] Simulator UI + endpoint
- [ ] Azure OpenAI recommendation text

### M4 — Polish & Demo
- [ ] Export PDF laporan
- [ ] Error states + loading skeletons
- [ ] Mobile responsive
- [ ] Demo script & mock data Bandung lengkap
- [ ] Final README + docs update