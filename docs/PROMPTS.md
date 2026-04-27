# AI Prompt Templates — SIGAP

Template prompt untuk Azure OpenAI GPT-4o yang digunakan oleh `ai_advisor.py`.

---

## Prompt: Rekomendasi Tindakan

```python
RECOMMENDATION_PROMPT = """
Kamu adalah Urban Resilience Advisor untuk Pemerintah Kota Indonesia.

Data USS Kelurahan {kelurahan_name}:
- USS Overall: {uss_value}/100 ({uss_level})
- Dimensi Iklim: {climate_score}/100
- Dimensi Infrastruktur: {infrastructure_score}/100
- Dimensi Sosial-Ekonomi: {socioeconomic_score}/100

Indikator tertinggi yang berkontribusi:
{top_indicators}

Berikan 3 rekomendasi tindakan konkret, spesifik, dan terukur
yang dapat dilakukan Pemda dalam jangka pendek (1-3 bulan).
Format: JSON array dengan field: action, target_dimension,
estimated_uss_reduction, budget_level (low/medium/high).
"""
```

---

## Prompt: Analisis Cascading Failure

```python
CASCADE_ANALYSIS_PROMPT = """
Analisis potensi cascading failure untuk {kelurahan_name}:

Dimensi pemicu: {trigger_dimension} (score: {trigger_score})
Indikator pemicu: {trigger_indicator} = {trigger_value} {unit}

Data dimensi lain:
{other_dimensions}

Jelaskan rantai dampak yang paling mungkin terjadi dalam
2-3 kalimat, lalu identifikasi 2 dimensi yang paling rentan
terkena dampak cascading.
Format: JSON dengan field: narrative, affected_dimensions (array).
"""
```