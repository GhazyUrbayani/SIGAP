# Product Requirements Document — SIGAP
**Version**: 2.0.0  
**Status**: Draft  
**Last Updated**: 2026-04-28  
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

## 4. Fitur Utama

### 4.1 Urban Stress Score (USS) Engine (P0 — Must Have)

**Deskripsi**: Model Ensemble (XGBoost / LightGBM / Random Forest — dibandingkan dan dipilih terbaik berdasarkan evaluasi RMSE/AUC) dikombinasikan dengan **Isolation Forest** untuk menghitung skor kerentanan **0–100** per kelurahan berdasarkan 3 dimensi: **Iklim**, **Infrastruktur**, dan **Sosial-Ekonomi**.

- Isolation Forest berfungsi sebagai **validasi anomali** untuk memastikan skor USS yang dihasilkan ensemble model tidak mengandung outlier yang tidak terdeteksi.
- Bobot dimensi dikalibrasi menggunakan model terpilih terhadap data historis kejadian bencana BPBD.

**User Stories**:
- Sebagai Analis, saya ingin melihat USS per kelurahan dalam bentuk peta warna agar saya dapat dengan cepat mengidentifikasi zona merah.
- Sebagai Admin, saya ingin mengkonfigurasi bobot dimensi USS agar model dapat disesuaikan dengan konteks kota yang berbeda.
- Sebagai Viewer, saya ingin melihat riwayat USS 12 bulan terakhir agar saya dapat memahami tren kerentanan.

**Acceptance Criteria**:
- [ ] USS dihitung ulang otomatis setiap ada trigger data baru
- [ ] USS ditampilkan dalam 3 zona warna: 🟢 Hijau (0–39), 🟡 Kuning (40–69), 🔴 Merah (70–100)
- [ ] Perubahan USS >10 poin dalam 24 jam memicu notifikasi
- [ ] Perhitungan selesai dalam <30 detik untuk 1 kota
- [ ] Perbandingan model (XGBoost, LightGBM, RF) terdokumentasi dengan metrik evaluasi

---

### 4.2 Cascading Failure Modeler (P0 — Must Have)

**Deskripsi**: Komponen yang mendeteksi **interaksi antar-dimensi**. Skor USS dikalkulasi (tidak hanya dijumlah linear) dengan **interaction term**, sehingga menghasilkan efek non-linear.

**Contoh**: Banjir tinggi × Infrastruktur buruk × Kemiskinan tinggi = skor melonjak **non-linear** (efek domino). Contoh rantai: Banjir parah (Iklim ↑) → Jalan rusak (Infrastruktur ↑) → Akses layanan kesehatan terhambat (Sosial ↑).

**User Stories**:
- Sebagai BPBD, saya ingin melihat "rantai kegagalan" yang mungkin terjadi agar saya dapat menyiapkan respons multi-dimensi.
- Sebagai Analis, saya ingin simulasi: "Jika debit sungai Cikapundung meningkat 200%, apa dampak cascading ke infrastruktur dan sosial?"

**Acceptance Criteria**:
- [ ] Interaction terms antar-dimensi (non-linear) terkalkulasi dalam model
- [ ] Skor melonjak jika ≥2 dimensi kritis bersamaan
- [ ] Feature Importance per interaction term tersedia untuk transparansi model
- [ ] Visualisasi graph/sankey diagram cascading antar dimensi
- [ ] Threshold trigger cascading dapat dikonfigurasi
- [ ] Histori cascading event tersimpan untuk audit

---

### 4.3 Dynamic Trigger System (P0 — Must Have)

**Deskripsi**: Pipeline otomatis yang menarik data **BMKG** (curah hujan mingguan, dll), mendeteksi **anomali** menggunakan z-score (> 2σ), dan memicu **pembaruan USS** jika threshold terlampaui.

**Trigger Levels**:
| Level | USS Range | Aksi |
|-------|-----------|------|
| **Watch** | 60–69 | Notifikasi email ke Analyst |
| **Warning** | 70–79 | Notifikasi email + in-app ke BPBD |
| **Emergency** | ≥80 | Push notification + laporan otomatis ke Kepala Daerah |

**User Stories**:
- Sebagai Admin, saya ingin mengatur threshold alert per kota agar sesuai dengan kondisi lokal.
- Sebagai BPBD, saya ingin menerima notifikasi ketika USS kelurahan mencapai level Warning.

**Acceptance Criteria**:
- [ ] Data BMKG ditarik otomatis per minggu (weekly pipeline)
- [ ] Deteksi anomali via z-score > 2σ berfungsi
- [ ] USS diperbarui otomatis jika threshold terlampaui
- [ ] Update USS ≤ 10 menit sejak trigger

---

### 4.4 Choropleth Dashboard Interaktif (P0 — Must Have)

**Deskripsi**: Dashboard utama berupa visualisasi **HeatMap** dengan zona 🟢 HIJAU / 🟡 KUNING / 🔴 MERAH yang dilengkapi **drill-down** per daerah kecil (RT/RW) dan grafik **tren historis**.

**User Stories**:
- Sebagai semua role, saya ingin melihat peta kota dengan warna kerentanan per kelurahan agar saya dapat memahami situasi secara visual.
- Sebagai Analis, saya ingin klik satu kelurahan dan melihat detail USS + breakdown per dimensi + tren historis.
- Sebagai Viewer, saya ingin filter peta berdasarkan dimensi tertentu (hanya iklim, hanya infrastruktur).

**Acceptance Criteria**:
- [ ] Choropleth HIJAU/KUNING/MERAH per kelurahan berfungsi
- [ ] Drill-down hingga level RT/RW tersedia
- [ ] Tren historis USS ≥30 hari ditampilkan dalam grafik
- [ ] Dashboard load ≤ 3 detik

---

### 4.5 Actionable Alert Engine (P0 — Must Have)

**Deskripsi**: Generator rekomendasi teks **natural language** (Bahasa Indonesia) per kelurahan yang masuk zona KUNING/MERAH. Alert menampilkan **penyebab**, **lokasi titik kritis**, dan **tenggat aksi**.

**Contoh Output**:
> *"Kelurahan X masuk ZONA MERAH karena anomali curah hujan +340% dari baseline, 3 titik drainase kritis teridentifikasi di RW 05, 09, 14 dan sekitarnya. Rekomendasi: inspeksi fisik dan siagakan tim BPBD dalam 48 jam."*

**User Stories**:
- Sebagai BPBD, saya ingin menerima rekomendasi teks yang langsung dapat dipahami tanpa keahlian teknis.
- Sebagai Analis, saya ingin mengetahui penyebab utama kenaikan USS beserta lokasi titik kritis.

**Acceptance Criteria**:
- [ ] Teks rekomendasi Bahasa Indonesia dihasilkan per kelurahan zona KUNING/MERAH
- [ ] Alert menampilkan penyebab, lokasi titik kritis, dan tenggat aksi
- [ ] Rekomendasi dapat dipahami oleh aparatur non data-science

---

### 4.6 Skenario Simulator (P1 — Should Have)

**Deskripsi**: Fitur **"bagaimana jika"** untuk perencana kota: simulasi dampak pembangunan infrastruktur terhadap USS **5 tahun ke depan**.

**User Stories**:
- Sebagai Bappeda, saya ingin simulasi: "Jika rasio tutupan lahan hijau naik 15%, bagaimana USS berubah?" agar saya dapat justifikasi investasi RTH.
- Sebagai PUPR, saya ingin simulasi: "Jika 30% jalan di Kecamatan Coblong diperbaiki, apa dampaknya ke USS infrastruktur?"

**Acceptance Criteria**:
- [ ] Simulasi "what if" parameter infrastruktur berfungsi
- [ ] Proyeksi USS 5 tahun ke depan ditampilkan
- [ ] Tampilan perbandingan baseline vs intervensi tersedia

---

### 4.7 Laporan & Export (P2 — Nice to Have)

- Export laporan PDF berisi ringkasan USS, peta, dan rekomendasi
- Export data CSV per kelurahan untuk analisis lanjut di Excel
- Template laporan resmi (letterhead Pemda)

---

## 5. Functional Requirements

| ID | Fitur | Requirement |
|----|-------|-------------|
| **FR-01** | USS Engine | Hitung skor 0–100 per kelurahan |
| **FR-01** | USS Engine | Bandingkan XGBoost, LightGBM, RF (pilih terbaik dengan evaluasi RMSE/AUC) |
| **FR-01** | USS Engine | Isolation Forest sebagai validasi anomali |
| **FR-02** | Cascading Modeler | Interaction terms antar-dimensi (non-linear) |
| **FR-02** | Cascading Modeler | Skor melonjak jika ≥2 dimensi kritis bersamaan |
| **FR-02** | Cascading Modeler | Feature Importance per interaction term |
| **FR-03** | Dynamic Trigger | Tarik data BMKG otomatis per minggu |
| **FR-03** | Dynamic Trigger | Deteksi anomali via z-score > 2σ |
| **FR-03** | Dynamic Trigger | Perbarui USS otomatis jika threshold terlampaui |
| **FR-04** | Dashboard | Choropleth HIJAU/KUNING/MERAH per kelurahan |
| **FR-04** | Dashboard | Drill-down RT/RW |
| **FR-04** | Dashboard | Tren historis USS ≥30 hari |
| **FR-05** | Alert Engine | Teks rekomendasi Bahasa Indonesia per kelurahan |
| **FR-05** | Alert Engine | Display penyebab, lokasi titik kritis, tenggat aksi |
| **FR-06** | Simulator | Simulasi "what if" parameter infrastruktur |
| **FR-06** | Simulator | Proyeksi USS 5 tahun ke depan |
| **FR-06** | Simulator | Tampilan baseline vs intervensi |

---

## 6. Non-Functional Requirements

| ID | Aspek | Requirement |
|----|-------|-------------|
| **NFR-01** | Performa | Update USS ≤ 10 menit sejak trigger |
| **NFR-01** | Performa | Dashboard load ≤ 3 detik |
| **NFR-02** | Skalabilitas | Handle 500+ kelurahan tanpa degradasi |
| **NFR-02** | Skalabilitas | Pipeline ETL modular & extensible |
| **NFR-03** | Resiliensi Data | Fallback BMKG → NASA IMERG otomatis |
| **NFR-03** | Resiliensi Data | Fallback BPS → PODES proxy otomatis |
| **NFR-04** | Usability | Dapat digunakan aparatur non data-science |
| **NFR-04** | Usability | Akses via browser tanpa instalasi |
| **NFR-05** | Auditabilitas | Pipeline reproducible & terdokumentasi |
| **NFR-05** | Auditabilitas | Log trigger tersimpan per update USS |
| **NFR-06** | Keamanan | HANYA data open-source publik |
| **NFR-06** | Keamanan | 0 data pribadi penduduk |

---

## 7. Tech Stack

| Teknologi | Fungsi |
|-----------|--------|
| **Azure Machine Learning** | Training, deployment, dan monitoring model anomaly detection (Isolation Forest) + ensemble classifier (XGBoost / LightGBM) |
| **Azure Event Hubs** | Ingest stream data BMKG real-time (curah hujan, suhu, kelembaban) |
| **Azure Maps** | Visualisasi choropleth dinamis — HeatMap layer-ed overlay multi-hazard |
| **Azure Synapse Analytics** | Pipeline ETL integrator data BMKG, BPS, OSM, dan PUPR |
| **Power BI Embedded** | Dashboard eksekutif untuk stakeholder (tanpa instalasi) |
| **Python (Pandas, Scikit-learn, GeoPandas)** | EDA saat development, preprocessing, feature engineering, spatial analysis |
| **FastAPI** | REST API back-end untuk integrasi data & display output |
| **PostgreSQL / PostGIS** | Database relasional dengan dukungan geospasial |
| **Redis** | Caching layer untuk performa dashboard |

### Dataset Open Source

| Sumber | Deskripsi |
|--------|-----------|
| **BMKG Open Data API** | Data iklim (curah hujan, suhu, kelembaban) |
| **BPS Statistik Kemiskinan 2023–2024** | Indikator sosial-ekonomi per wilayah |
| **OpenStreetMap Indonesia** | Kondisi jalan & drainase |
| **BNPB GIS Disaster History** | Histori kejadian bencana |
| **Riskesdas** | Indeks kesehatan per kelurahan |

---

## 8. Arsitektur Solusi (High Level)

```
[Data Sources]              [Backend]              [Frontend]
BMKG API ──────────► Data Ingestion    ──► React Dashboard
BPS API  ──────────► USS Engine        ──► Choropleth Map
BPBD Data ─────────► ML Model         ──► Alert Panel
OSM API  ──────────► Alert Engine      ──► Simulator UI
                     REST API (FastAPI)
                     PostgreSQL/PostGIS
                     Redis Cache

[Azure Services]
Azure ML ──────────► Model Training & Deployment
Azure Event Hubs ──► Real-time Data Ingestion
Azure Synapse ─────► ETL Pipeline
Azure Maps ────────► Geospatial Visualization
Power BI Embedded ─► Executive Dashboard
```

---

## 9. Cara Penggunaan Product

### Flow Pengguna (Petugas Pemda / BPBD)

#### Langkah 1 — Login Dashboard
Pengguna mengakses portal SIGAP melalui **browser**. Login menggunakan akun Pemda (integrasi SSO atau credential demo). **Tidak diperlukan instalasi software tambahan.**

#### Langkah 2 — Lihat Peta Urban Stress Score
Halaman utama menampilkan peta kota dengan warna per kelurahan:
- 🟢 **Hijau (USS 0–39)**: Aman, tidak ada aksi darurat
- 🟡 **Kuning (USS 40–69)**: Waspada, rekomendasikan inspeksi rutin
- 🔴 **Merah (USS 70–100)**: Darurat, aksi segera diperlukan

#### Langkah 3 — Drill-down Kelurahan
Klik satu kelurahan → tampil panel detail:
- Skor tiap dimensi (Iklim / Infrastruktur / Sosial-Ekonomi)
- Grafik tren USS 30 hari terakhir
- Peta titik-titik infrastruktur kritis

#### Langkah 4 — Baca Rekomendasi Aksi
Setiap kelurahan zona KUNING/MERAH dilengkapi **teks rekomendasi spesifik**, ditampilkan dalam Bahasa Indonesia yang dapat langsung dipahami aparatur **tanpa keahlian teknis**.

#### Langkah 5 — Jalankan Simulasi
Petugas perencana dapat menggunakan fitur **simulator** untuk melihat proyeksi USS jika infrastruktur di titik tertentu diperbaiki atau anggaran dialihkan.

---

## 10. Dependencies & Integrasi

| Service | Tipe | Endpoint | SLA |
|---------|------|----------|-----|
| BMKG Open Data | REST API publik | `https://data.bmkg.go.id/api/` | Best effort |
| BPS API | REST API publik | `https://webapi.bps.go.id/v1/` | Best effort |
| Azure Maps | SDK | Azure Subscription | 99.9% |
| Azure OpenAI | API | Azure Subscription | 99.9% |
| Azure ML | SDK | Azure Subscription | 99.9% |
| Azure Event Hubs | SDK | Azure Subscription | 99.9% |
| Azure Synapse | SDK | Azure Subscription | 99.9% |
| OSM Overpass | REST API publik | `https://overpass-api.de/` | Best effort |
| NASA IMERG | REST API publik | Fallback untuk data iklim | Best effort |

---

## 11. Risiko & Mitigasi

| Risiko | Kemungkinan | Dampak | Mitigasi |
|--------|-------------|--------|----------|
| Data BMKG tidak granular per kelurahan | Tinggi | Tinggi | Interpolasi spasial + fallback ke kecamatan |
| API BMKG down | Medium | Tinggi | Fallback otomatis ke NASA IMERG |
| Data BPS tidak tersedia | Medium | Tinggi | Fallback otomatis ke PODES proxy |
| API eksternal down saat demo | Medium | Tinggi | Redis cache + mock data fallback |
| Model ML overfit ke Bandung | Medium | Medium | Cross-validasi + fitur yang generalizable |
| Waktu compute USS terlalu lama | Rendah | Medium | Background worker + hasil di-cache Redis |

---

## 12. Metrics Keberhasilan

| Metric | Target |
|--------|--------|
| USS computation time | <30 detik per kota |
| USS update latency | ≤10 menit sejak trigger |
| Alert false positive rate | <15% |
| Dashboard load time | <3 detik |
| Data coverage kelurahan | >90% kelurahan pilot |
| Kelurahan capacity | 500+ tanpa degradasi |
| Juri score (kompetisi) | Top 3 finalis |