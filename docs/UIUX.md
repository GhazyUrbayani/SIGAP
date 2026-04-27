# UIUX.md — SIGAP Design System & UI/UX Specification

> Versi: 1.0 | Terakhir diperbarui: April 2026
> Prinsip utama: **Craft over template. Editorial over dashboard. Human over AI.**
> Referensi: 21st.dev component philosophy, Anti-AI-generated UI principles

---

## 1. Design Philosophy

SIGAP bukan dashboard monitoring biasa. Ia adalah **ruang kerja keputusan** bagi
aparatur pemerintah yang harus bertindak cepat dan tepat. UI-nya harus terasa
seperti *instrument panel pesawat yang dibuat oleh insan*, bukan
*template SaaS yang digenerate AI*.

### 1.1 Tiga Prinsip Utama

**Editorial over Generic**
Setiap elemen harus punya *opini visual*. Gunakan whitespace yang ekspresif,
bukan sekedar padding matematis. Typography memimpin layout, bukan sebaliknya.

**Data Clarity over Decoration**
Warna digunakan semantik (HIJAU/KUNING/MERAH punya makna, bukan estetika).
Tidak ada gradien dekoratif. Chart dan peta adalah hero, bukan ornamen.

**Tension & Weight**
Zona MERAH harus *terasa berbahaya*. Zona HIJAU harus *terasa tenang*.
UI harus mentransfer urgensi dari data ke pembaca secara emosional.

---

## 2. Design Tokens

```css
/* ─── TYPOGRAPHY ──────────────────────────────────────── */
--font-display:  'Syne', 'Plus Jakarta Sans', sans-serif;   /* headline, nav */
--font-body:     'Inter', 'DM Sans', sans-serif;            /* body, label */
--font-data:     'JetBrains Mono', 'IBM Plex Mono', monospace; /* angka, kode, skor */

/* Scale — Minor Third (1.250) */
--text-xs:    0.64rem;   /* 10.2px — meta, badge */
--text-sm:    0.8rem;    /* 12.8px — caption */
--text-base:  1rem;      /* 16px   — body */
--text-lg:    1.25rem;   /* 20px   — subheading */
--text-xl:    1.563rem;  /* 25px   — heading */
--text-2xl:   1.953rem;  /* 31px   — page title */
--text-3xl:   2.441rem;  /* 39px   — hero number / USS score */

--font-weight-normal:   400;
--font-weight-medium:   500;
--font-weight-semibold: 600;
--font-weight-bold:     700;
--font-weight-black:    900; /* dipakai untuk USS score number */

--line-height-tight:    1.2;
--line-height-normal:   1.5;
--line-height-relaxed:  1.75;
--letter-spacing-wide:  0.08em; /* dipakai untuk label uppercase */

/* ─── COLOR SYSTEM ────────────────────────────────────── */
/* Tidak menggunakan generic blue-500 atau AI defaults */

/* Neutral — warm undertone, bukan cold gray */
--color-bg:              #F7F6F3;  /* warm off-white, bukan #FAFAFA */
--color-bg-subtle:       #EFEDE8;
--color-surface:         #FFFFFF;
--color-surface-raised:  #FDFDFC;
--color-border:          #E8E4DC;
--color-border-strong:   #C9C4B8;

/* Text */
--color-text-primary:    #1C1916;  /* warm near-black */
--color-text-secondary:  #6B6560;
--color-text-tertiary:   #9C968F;
--color-text-inverse:    #FAFAF8;

/* Semantic — USS Zone Colors */
/* HIJAU (USS 0–39): tenang, aman */
--color-zone-green:       #1A7A4A;
--color-zone-green-bg:    #EBFAF3;
--color-zone-green-muted: #D1F0E0;

/* KUNING (USS 40–69): waspada, perhatian */
--color-zone-yellow:       #B45309;  /* amber, bukan yellow biasa */
--color-zone-yellow-bg:    #FFF8EB;
--color-zone-yellow-muted: #FDECC8;

/* MERAH (USS 70–100): kritis, darurat */
--color-zone-red:       #B91C1C;
--color-zone-red-bg:    #FFF1F0;
--color-zone-red-muted: #FFD9D9;
--color-zone-red-pulse: #EF4444; /* untuk pulse animation */

/* Brand accent — slate biru kehijauan, bukan electric blue */
--color-accent:         #1B4F72;
--color-accent-hover:   #154060;
--color-accent-subtle:  #E8F0F7;

/* ─── SPACING ─────────────────────────────────────────── */
/* 4px base grid */
--space-1:  0.25rem;   /* 4px */
--space-2:  0.5rem;    /* 8px */
--space-3:  0.75rem;   /* 12px */
--space-4:  1rem;      /* 16px */
--space-5:  1.25rem;   /* 20px */
--space-6:  1.5rem;    /* 24px */
--space-8:  2rem;      /* 32px */
--space-10: 2.5rem;    /* 40px */
--space-12: 3rem;      /* 48px */
--space-16: 4rem;      /* 64px */

/* ─── BORDER RADIUS ───────────────────────────────────── */
/* Consistent hierarchy, bukan semua rounded-xl */
--radius-sm:   4px;   /* badge, tag */
--radius-md:   8px;   /* button, input */
--radius-lg:  12px;   /* card */
--radius-xl:  16px;   /* modal, panel besar */
--radius-full: 9999px; /* pill, avatar */

/* ─── SHADOW ──────────────────────────────────────────── */
/* Warm shadow (sedikit amber undertone) */
--shadow-xs: 0 1px 2px rgba(28,25,22,0.06);
--shadow-sm: 0 1px 3px rgba(28,25,22,0.10), 0 1px 2px rgba(28,25,22,0.06);
--shadow-md: 0 4px 6px rgba(28,25,22,0.07), 0 2px 4px rgba(28,25,22,0.06);
--shadow-lg: 0 10px 15px rgba(28,25,22,0.08), 0 4px 6px rgba(28,25,22,0.05);
--shadow-zone-red: 0 0 0 3px rgba(185,28,28,0.15); /* focus ring kritis */
```

---

## 3. Layout Architecture

### 3.1 App Shell
┌─────────────────────────────────────────────────────────────────┐
│ SIDEBAR (240px fixed) │ MAIN CONTENT AREA │
│ ┌──────────────────────┐ │ ┌─────────────────────────────┐ │
│ │ SIGAP logo + kota │ │ │ PAGE HEADER │ │
│ │ ─────────────────── │ │ │ Judul + breadcrumb + aksi │ │
│ │ Nav items: │ │ ├─────────────────────────────┤ │
│ │ - Dashboard │ │ │ │ │
│ │ - Alert Log │ │ │ CONTENT │ │
│ │ - Simulator │ │ │ │ │
│ │ - Data Sources │ │ │ │ │
│ │ ─────────────────── │ │ │ │ │
│ │ USS Summary Mini │ │ │ │ │
│ │ (zona count badges) │ │ └─────────────────────────────┘ │
│ └──────────────────────┘ │ │
└─────────────────────────────────────────────────────────────────┘

text

**Anti-AI-generated rule:** Sidebar tidak menggunakan gradient purple/blue.
Background sidebar: `--color-bg-subtle` (#EFEDE8) dengan left border
`2px solid --color-border-strong`.

### 3.2 Grid System
Dashboard: CSS Grid asymmetric
- Peta (choropleth): 60% lebar
- Panel detail/alert: 40% lebar
- Bukan 50/50 — asimetri membuat mata lebih natural bergerak

Alert Page: 1 kolom full, editorial layout (mirip news feed)

Simulator: 2 kolom equal — input kiri, output chart kanan

text

### 3.3 Anti-grid Moments (21st.dev inspired)
Di halaman Dashboard, USS Score kartu kelurahan terpilih menggunakan
**overlapping element** — angka USS besar (font 3xl, font-weight black)
overlapping ke tepi card, bukan centered di dalam box. Ini membuat data
terasa lebih berat dan nyata. [web:152]

---

## 4. Component Specifications

### 4.1 USSScoreDisplay — Komponen Utama

USS Score bukan sekadar angka. Ia adalah **statement visual** pertama yang
dilihat pengguna ketika membuka kelurahan.
Visual anatomy:
┌────────────────────────────────────┐
│ KELURAHAN SUKASARI ● MERAH│ ← nama + zone badge
│ │
│ 87 │ ← USS number: font-data 3xl black
│ ──── Urban Stress Score ──── │ ← label: uppercase xs, letter-spacing
│ │
│ ↑ 12 poin dari minggu lalu │ ← delta indicator
│ │
│ Iklim ████████░░ 79 │
│ Infra ██████░░░░ 61 │ ← 3 dimension bars
│ Sosek █████████░ 84 │
└────────────────────────────────────┘

text

**Rules:**
- Angka USS: font-data, weight 900, warna sesuai zona (merah jika 70+)
- Jika USS ≥ 70: card memiliki `border-left: 3px solid --color-zone-red`
  dan subtle red background. Tidak menggunakan full red card.
- Delta indicator: `↑` merah jika naik, `↓` hijau jika turun

### 4.2 Choropleth Map (Azure Maps)
Zone styling:
HIJAU (0–39): fill #1A7A4A, opacity 0.55
KUNING (40–69): fill #B45309, opacity 0.55
MERAH (70–100):fill #B91C1C, opacity 0.70
MERAH kritis (≥85): tambahkan CSS pulse animation pada border

Hover state:
- Opacity naik ke 0.85
- Tooltip muncul: nama kelurahan + USS score + zona
- Cursor: pointer

Tooltip format:
┌─────────────────────┐
│ Kel. Cicendo │
│ USS: 74 ● MERAH │
│ Klik untuk detail │
└─────────────────────┘

Anti-AI rule:
- Tidak menggunakan default Leaflet popup bubble
- Tooltip: custom styled, warm background surface, shadow-md
- Map tile: menggunakan style "grayscale" dari Azure Maps agar
warna zona lebih terbaca dan tidak bertabrakan dengan warna tile

text

### 4.3 AlertCard

Alert bukan notifikasi biasa — ia adalah **instruksi darurat**.
Desain harus mengkomunikasikan urgensi tanpa terasa panik.
┌──────────────────────────────────────────────────────┐
│ ● ZONA MERAH · Diperbarui 14 menit lalu │
│ │
│ Kelurahan Cicendo — USS 74 │ ← semibold lg
│ │
│ Anomali curah hujan +340% dari baseline. 3 titik │ ← body text normal
│ drainase kritis teridentifikasi di RW 05, 09, 14. │
│ │
│ Rekomendasi: Inspeksi fisik & siagakan BPBD │ ← bold, accent color
│ dalam 48 jam. │
│ │
│ [Lihat Detail] [Tandai Ditangani] │ ← 2 actions
└──────────────────────────────────────────────────────┘

Border kiri: 3px solid --color-zone-red
Background: --color-zone-red-bg (#FFF1F0)
Bukan: full red card, icon warning besar, atau animasi berlebihan

text

### 4.4 TrendChart (Recharts)
Type: Area chart (bukan line chart — area memberi kesan berat/volume)
X-axis: 30 hari terakhir, label "DD MMM"
Y-axis: 0–100, gridlines tipis (opacity 0.3)

Area fill:
- Jika USS saat ini ≥ 70: fill gradient merah (#B91C1C → transparent)
- Jika USS 40–69: fill gradient amber
- Jika USS < 40: fill gradient hijau

Anti-AI rule:
- Tidak menggunakan default Recharts blue
- Stroke width: 2px (bukan 1px terlalu tipis atau 3px terlalu tebal)
- Tooltip: custom component, sama dengan design token (bukan default box abu)
- Dot pada data point: hanya muncul saat hover, radius 4px

text

### 4.5 ScenarioSimulator
Layout: 2 kolom

Kiri — Parameter Panel:
- Judul: "Skenario Intervensi"
- Slider untuk setiap parameter infrastruktur:
- Peningkatan drainase (0–100%)
- Perbaikan jalan (0–100%)
- Program sosial (0–100%)
- Proyeksi dalam: 12 / 24 / 36 / 60 bulan (segmented control)
- Tombol "Jalankan Simulasi" — full width, accent color

Kanan — Projection Chart:
- 2 lines: "Baseline" (putus-putus, gray) vs "Intervensi" (solid, accent)
- Label langsung di ujung garis, bukan di legend terpisah
- Annotation: tanda panah + teks "Estimasi penurunan USS: -18 poin"
di titik divergensi terbesar antara 2 garis

text

### 4.6 Navigation Sidebar
Logo area:
SIGAP ← font-display, weight 700, 18px
Kota Bandung ▾ ← kota selector, text-sm, secondary color

Nav items (active state):
Background: --color-accent-subtle
Border-left: 3px solid --color-accent
Font-weight: 600
BUKAN: blue pill background seperti default Tailwind sidebar tutorial

Nav items (inactive):
Hover background: --color-border (#E8E4DC)
Transition: 150ms ease

Bottom section sidebar:
Mini USS summary (3 badge: jumlah kelurahan per zona)
Format: "● 12 MERAH ● 7 KUNING ● 31 HIJAU"
Font: font-data xs, sesuai warna zona

text

---

## 5. States yang Wajib Di-handle

| State | Komponen | Tampilan |
|---|---|---|
| Loading peta | ChoroplethMap | Skeleton gray dengan animated shimmer — BUKAN spinner di tengah |
| Loading USS | USSScoreDisplay | Skeleton 3 baris, lebar bervariasi (bukan uniform) |
| Data BMKG unavailable | TriggerBadge | Badge "Data BMKG tunda — menggunakan IMERG" amber, non-blocking |
| Kelurahan tanpa data | USSScoreDisplay | "Data belum tersedia" dengan ikon jam, bukan error merah |
| Anomali baru terdeteksi | Sidebar mini USS | Badge angka merah bergetar (shake animation 0.5s, sekali saja) |
| Alert ditangani | AlertCard | Strikethrough halus + opacity 0.5, tidak hilang langsung |
| Simulasi berjalan | ScenarioChart | Skeleton chart animasi + teks "Menghitung proyeksi..." |
| Koneksi gagal | Seluruh app | Toast bottom-right: "Koneksi terputus. Data terakhir: 14 mnt lalu" |
| Empty state alert | AlertPage | Ilustrasi minimal + "Semua kelurahan dalam zona aman" hijau |

---

## 6. Micro-interactions & Motion

Gunakan motion secara **hemat dan bermakna**. Tidak ada animasi dekoratif.

```css
/* Transition defaults */
--transition-fast:   100ms ease;
--transition-base:   200ms ease;
--transition-slow:   350ms ease;

/* Penggunaan:
   - Hover state change:    --transition-fast
   - Card expand/collapse:  --transition-base
   - Page transition:       --transition-slow (fade only, tidak slide berlebihan)
   - USS score update:      counter animation 800ms ease-out (angka berputar)
*/

/* Pulse animation untuk zona merah kritis (USS ≥ 85) */
@keyframes zone-pulse {
  0%, 100% { box-shadow: 0 0 0 0 rgba(185,28,28,0.4); }
  50%       { box-shadow: 0 0 0 8px rgba(185,28,28,0); }
}
/* Periode: 2s, infinite — HANYA pada card USS kritis, bukan semua MERAH */

/* Score update counter */
@keyframes count-up {
  from { opacity: 0; transform: translateY(4px); }
  to   { opacity: 1; transform: translateY(0); }
}
```

**Anti-AI rules untuk motion:**
- Tidak ada `transition: all 300ms` — selalu spesifik properti
- Tidak ada hover scale transform pada card data (terasa mainan)
- Page navigation: fade opacity saja, tidak slide dari samping

---

## 7. Typography Usage Rules
Page title (h1): font-display, text-2xl, weight 700
Section heading (h2): font-display, text-xl, weight 600
Subsection (h3): font-body, text-lg, weight 600
Body text: font-body, text-base, weight 400, line-height relaxed
Label / meta: font-body, text-sm, weight 500, UPPERCASE, letter-spacing-wide
Data angka (USS, %): font-data, weight sesuai konteks (700 untuk highlight, 400 untuk tabel)
Badge text: font-body, text-xs, weight 600, UPPERCASE

text

**Anti-AI font pairing rules:**
- Jangan pakai Inter saja untuk semua — campur Syne untuk heading
- Jangan pakai font-data (monospace) untuk label non-angka
- Jangan lebih dari 3 font family dalam satu halaman

---

## 8. Cara Integrasi dengan 21st.dev Magic

Untuk komponen yang tidak di-spec di dokumen ini, gunakan 21st.dev Magic
agar mendapat variasi terbaik secara otomatis: [web:143][web:145][web:153]

```bash
# Install 21st.dev Magic MCP di Antigravity / VS Code / Cursor
npx @21st-dev/magic@latest init

# Atau install manual sebagai MCP server
```
Prompt pattern untuk 21st.dev Magic:
"Generate a [component name] component using React + TypeScript + Tailwind.
Style constraints:

Background: warm off-white #F7F6F3, NOT cool gray

Typography: Syne for headings, Inter for body, JetBrains Mono for numbers

Border radius: 8px for interactive elements, 12px for cards

No gradients unless data-driven (zone colors only)

Shadow: warm undertone rgba(28,25,22,...)
Semantic colors only: green #1A7A4A, amber #B45309, red #B91C1C
Generate 3 variations, pick the one that feels most editorial, not generic."

text

**Komponen dari 21st.dev yang bisa langsung dipakai / dimodifikasi:**
- `animated-number` → untuk counter USS score update [web:142]
- `data-table` → untuk tabel drill-down RT/RW
- `toast-notification` → untuk koneksi gagal / alert baru
- `segmented-control` → untuk pilihan proyeksi 12/24/36/60 bulan
- `skeleton-loader` → untuk loading states semua komponen

---

## 9. Aksesibilitas (WCAG AA Minimum)
Contrast ratio:
- Text normal (< 18px): minimum 4.5:1
- Text besar (≥ 18px bold): minimum 3:1
- Zone colors sudah memenuhi:
- #1A7A4A on #EBFAF3: ratio 5.8:1 ✅
- #B45309 on #FFF8EB: ratio 4.7:1 ✅
- #B91C1C on #FFF1F0: ratio 5.1:1 ✅

Focus visible:
- Semua interactive element: focus ring 2px offset 2px
- Warna focus: --color-accent (#1B4F72)
- JANGAN hilangkan outline focus untuk estetika

Keyboard navigation:
- Sidebar nav: Tab + Enter
- Map kelurahan: Tab untuk cycle, Enter untuk select
- Alert card actions: Tab accessible

Screen reader:
- USS score: aria-label="Urban Stress Score 74 dari 100, zona merah"
- Zone badge: role="status"
- Alert card: aria-live="polite" untuk update otomatis

text

---

## 10. Anti-Patterns — LARANGAN

Berdasarkan fingerprints AI-generated UI 2024–2025 yang harus dihindari: [web:150][web:146]
❌ DILARANG:
- Gradient background purple/blue/teal pada hero atau sidebar
- Card dengan rounded-2xl atau rounded-3xl (terlalu bubbly)
- Icon set generic Material Icons atau Heroicons tanpa customisasi
- Color palette: blue-500, purple-600, emerald-500 (terlalu "AI default")
- Setiap card punya shadow — hanya card interaktif yang punya shadow
- Font Inter untuk SEMUA text (terasa generic)
- Animasi scale-105 pada hover card
- Loading spinner di tengah halaman untuk setiap state
- Tabel dengan striped rows abu-abu dan border semua sisi
- Button dengan gradient fill (kecuali ada brand reason yang kuat)
- Semua spacing uniform — variasikan untuk ritme visual
- Monospace font untuk label non-data (terasa "hacker cosplay")

text

---

## 11. File & Folder Konvensi Frontend
src/
├── styles/
│ ├── tokens.css ← semua design tokens di atas
│ ├── globals.css ← reset + font import
│ └── components.css ← utility classes komponen (opsional)
├── components/
│ ├── ui/ ← primitives (Button, Badge, Card, Input)
│ ├── map/ ← ChoroplethMap, MapTooltip, ZoneLegend
│ ├── uss/ ← USSScoreDisplay, DimensionBar, DeltaIndicator
│ ├── alert/ ← AlertCard, AlertList, AlertBadge
│ ├── simulator/ ← ScenarioPanel, ProjectionChart
│ └── layout/ ← Sidebar, PageHeader, AppShell
└── lib/
├── colors.ts ← fungsi getZoneColor(score: number)
└── formatters.ts ← formatUSS, formatDelta, formatDate