# Product Requirements Document — SIGAP
**Version**: 1.0.0  
**Status**: Draft  
**Last Updated**: 2026-04-27  
**Owner**: SIGAP Team

---

## 1. Overview

### 1.1 Latar Belakang
Pemerintah daerah Indonesia selama ini mengalokasikan anggaran penanganan bencana secara **reaktif** — bergerak setelah krisis terjadi, bukan sebelumnya. Hal ini disebabkan tidak adanya satu sistem terpadu yang mengintegrasikan data iklim, infrastruktur, dan sosial-ekonomi menjadi satu skor kerentanan yang actionable.

SIGAP (Smart Integrated Geo-Analytics for Urban Pressure) hadir untuk mengisi gap ini dengan menghadirkan **Urban Stress Score (USS)** per kelurahan/kecamatan, yang memungkinkan Pemda mengidentifikasi zona risiko tinggi sebelum krisis terjadi.

### 1.2 Problem Statement
> **"Bagaimana cara mengidentifikasi wilayah perkotaan yang paling rentan terhadap kegagalan berantai (flooding + infrastruktur + tekanan sosial-ekonomi), sehingga perencana kota dapat memprioritaskan investasi resiliensi sebelum krisis?"**

### 1.3 Solusi
Aplikasi web analitik berbasis geospasial yang:
1. Mengagregasi data multi-sumber (BMKG, BPS, BPBD, OSM)
2. Menghitung USS per kelurahan menggunakan model ML
3. Mendeteksi potensi cascading failure antar dimensi
4. Menghasilkan alert dan rekomendasi tindakan yang spesifik
5. Memungkinkan simulasi skenario kebijakan

---

## 2. Goals & Non-Goals

### Goals
- ✅ USS Engine yang dapat dihitung ulang otomatis ketika data baru masuk
- ✅ Peta choropleth interaktif dengan drill-down per wilayah
- ✅ Alert engine berbasis threshold dengan notifikasi
- ✅ Cascading failure modeler (korelasi antar dimensi)
- ✅ Skenario simulator untuk evaluasi kebijakan
- ✅ Export laporan PDF/CSV untuk kebutuhan Pemda
- ✅ Autentikasi berbasis role (Admin, Analyst, Viewer)

### Non-Goals
- ❌ Tidak membangun sensor IoT fisik (data dari API eksternal)
- ❌ Tidak menyediakan fitur manajemen APBD/keuangan daerah
- ❌ Tidak menangani data real-time sub-menit (refresh minimum 1 jam)
- ❌ Tidak menjadi platform GIS umum (fokus pada Urban Resilience)

---

## 3. User Personas

| Persona | Jabatan | Kebutuhan Utama | Pain Point |
|---------|---------|-----------------|------------|
| **Andi** | Kepala BPBD Kota Bandung | Melihat zona risiko banjir + infrastruktur sebelum musim hujan | Data terpisah-pisah, tidak ada early warning terpadu |
| **Rini** | Analis Bappeda | Membuat laporan kerentanan untuk RPJMD | Proses manual 2-3 minggu per laporan |
| **Dani** | Staf Dinas PUPR | Memvalidasi kondisi infrastruktur dan kontribusinya ke risiko | Tidak tahu wilayah mana yang harus diprioritaskan |
| **Super Admin** | Tim IT Pemda | Mengelola user, data source, dan konfigurasi sistem | Tidak ada sistem terpusat |

---

## 4. Fitur & User Stories

### 4.1 Urban Stress Score Engine (P0 — Must Have)

**Deskripsi**: Engine yang menghitung skor kerentanan 0–100 per kelurahan berdasarkan tiga dimensi: Iklim, Infrastruktur, dan Sosial-Ekonomi.

**Formula dasar**:
USS = w₁ × Climate_Score + w₂ × Infrastructure_Score + w₃ × SocioEconomic_Score

text
Bobot (w) dikalibrasi menggunakan XGBoost Regressor terhadap data historis kejadian bencana BPBD.

**User Stories**:
- Sebagai Analis, saya ingin melihat USS per kelurahan dalam bentuk peta warna agar saya dapat dengan cepat mengidentifikasi zona merah.
- Sebagai Admin, saya ingin mengkonfigurasi bobot dimensi USS agar model dapat disesuaikan dengan konteks kota yang berbeda.
- Sebagai Viewer, saya ingin melihat riwayat USS 12 bulan terakhir agar saya dapat memahami tren kerentanan.

**Acceptance Criteria**:
- [ ] USS dihitung ulang otomatis setiap jam melalui cron job
- [ ] USS ditampilkan dalam 5 kategori warna: Sangat Rendah (hijau) → Sangat Tinggi (merah)
- [ ] Perubahan USS >10 poin dalam 24 jam memicu notifikasi
- [ ] Perhitungan selesai dalam <30 detik untuk 1 kota

---

### 4.2 Cascading Failure Modeler (P0 — Must Have)

**Deskripsi**: Mendeteksi korelasi antar dimensi yang dapat menyebabkan efek domino. Contoh: Banjir parah (Iklim ↑) → Jalan rusak (Infrastruktur ↑) → Akses layanan kesehatan terhambat (Sosial ↑).

**User Stories**:
- Sebagai BPBD, saya ingin melihat "rantai kegagalan" yang mungkin terjadi agar saya dapat menyiapkan respons multi-dimensi.
- Sebagai Analis, saya ingin simulasi: "Jika debit sungai Cikapundung meningkat 200%, apa dampak cascading ke infrastruktur dan sosial?"

**Acceptance Criteria**:
- [ ] Visualisasi graph/sankey diagram cascading antar dimensi
- [ ] Threshold trigger cascading dapat dikonfigurasi
- [ ] Histori cascading event tersimpan untuk audit

---

### 4.3 Dynamic Trigger System (P1 — Should Have)

**Deskripsi**: Alert otomatis berbasis threshold USS dan indikator spesifik.

**Trigger Levels**:
| Level | USS | Aksi |
|-------|-----|------|
| **Watch** | 60–69 | Notifikasi email ke Analyst |
| **Warning** | 70–79 | Notifikasi email + in-app ke BPBD |
| **Emergency** | ≥80 | Push notification + laporan otomatis ke Kepala Daerah |

**User Stories**:
- Sebagai Admin, saya ingin mengatur threshold alert per kota agar sesuai dengan kondisi lokal.
- Sebagai BPBD, saya ingin menerima notifikasi WhatsApp/email ketika USS kelurahan mencapai level Warning.

---

### 4.4 Choropleth Dashboard (P0 — Must Have)

**Deskripsi**: Dashboard utama berbasis peta interaktif dengan layer USS, indikator per dimensi, dan drill-down per wilayah.

**User Stories**:
- Sebagai semua role, saya ingin melihat peta Bandung dengan warna kerentanan per kelurahan agar saya dapat memahami situasi secara visual.
- Sebagai Analis, saya ingin klik satu kelurahan dan melihat detail USS + breakdown per dimensi + tren historis.
- Sebagai Viewer, saya ingin filter peta berdasarkan dimensi tertentu (hanya iklim, hanya infrastruktur).

---

### 4.5 Skenario Simulator (P1 — Should Have)

**Deskripsi**: Simulator "what-if" yang memungkinkan pengguna mengubah nilai indikator dan melihat dampak terhadap USS.

**User Stories**:
- Sebagai Bappeda, saya ingin simulasi: "Jika rasio tutupan lahan hijau naik 15%, bagaimana USS berubah?" agar saya dapat justifikasi investasi RTH.
- Sebagai PUPR, saya ingin simulasi: "Jika 30% jalan di Kecamatan Coblong diperbaiki, apa dampaknya ke USS infrastruktur?"

---

### 4.6 Laporan & Export (P2 — Nice to Have)

- Export laporan PDF berisi ringkasan USS, peta, dan rekomendasi
- Export data CSV per kelurahan untuk analisis lanjut di Excel
- Template laporan resmi (letterhead Pemda)

---

## 5. Arsitektur Solusi (High Level)
[Data Sources] [Backend] [Frontend]
BMKG API ──────────► Data Ingestion ──► React Dashboard
BPS API ──────────► USS Engine ──► Choropleth Map
BPBD Data ──────────► ML Model ──► Alert Panel
OSM API ──────────► Alert Engine ──► Simulator UI
REST API (FastAPI)
PostgreSQL/PostGIS
Redis Cache

text

---

## 6. Requirements Non-Fungsional

| Kategori | Requirement |
|----------|-------------|
| **Performance** | Dashboard load <3s, API response <500ms (p95) |
| **Availability** | Uptime 99% (development target) |
| **Security** | JWT Auth, RBAC, input sanitization, HTTPS |
| **Scalability** | Modular service, horizontal scale ready |
| **Accessibility** | WCAG 2.1 AA untuk warna peta |
| **Data Freshness** | Refresh data maksimal setiap 1 jam |

---

## 7. Dependencies & Integrasi

| Service | Tipe | Endpoint | SLA |
|---------|------|----------|-----|
| BMKG Open Data | REST API publik | `https://data.bmkg.go.id/api/` | Best effort |
| BPS API | REST API publik | `https://webapi.bps.go.id/v1/` | Best effort |
| Azure Maps | SDK | Azure Subscription | 99.9% |
| Azure OpenAI | API | Azure Subscription | 99.9% |
| OSM Overpass | REST API publik | `https://overpass-api.de/` | Best effort |

---

## 8. Risiko & Mitigasi

| Risiko | Kemungkinan | Dampak | Mitigasi |
|--------|-------------|--------|----------|
| Data BMKG tidak granular per kelurahan | Tinggi | Tinggi | Interpolasi spasial + fallback ke kecamatan |
| API eksternal down saat demo | Medium | Tinggi | Redis cache + mock data fallback |
| Model ML overfit ke Bandung | Medium | Medium | Cross-validasi + fitur yang generalizable |
| Waktu compute USS terlalu lama | Rendah | Medium | Background worker + hasil di-cache Redis |

---

## 9. Metrics Keberhasilan

| Metric | Target |
|--------|--------|
| USS computation time | <30 detik per kota |
| Alert false positive rate | <15% |
| Dashboard load time | <3 detik |
| Data coverage kelurahan | >90% kelurahan pilot |
| Juri score (kompetisi) | Top 3 finalis |