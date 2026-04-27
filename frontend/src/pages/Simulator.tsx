import { useState } from 'react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  ReferenceLine,
} from 'recharts';
import { Header } from '../components/layout/Header';
import { useUSSLatest } from '../hooks/useUSS';
import api from '../lib/api';
import type { ScenarioResponse } from '../types/uss';

export default function Simulator() {
  const { data: ussData } = useUSSLatest();
  const [selectedKelId, setSelectedKelId] = useState('');
  const [drainase, setDrainase] = useState(30);
  const [roadRepair, setRoadRepair] = useState(20);
  const [socialProgram, setSocialProgram] = useState(15);
  const [months, setMonths] = useState(36);
  const [result, setResult] = useState<ScenarioResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const monthOptions = [12, 24, 36, 60];

  const runSimulation = async () => {
    if (!selectedKelId) {
      setError('Pilih kelurahan terlebih dahulu');
      return;
    }
    setLoading(true);
    setError('');
    try {
      const res = await api.post<ScenarioResponse>('/uss/scenario', {
        kelurahan_id: selectedKelId,
        drainase_improvement: drainase / 100,
        road_repair: roadRepair / 100,
        social_program: socialProgram / 100,
        projection_months: months,
      });
      setResult(res.data);
    } catch {
      setError('Simulasi gagal. Pastikan kelurahan memiliki data USS.');
    } finally {
      setLoading(false);
    }
  };

  // Merge baseline + intervention for chart
  const chartData = result
    ? result.baseline_projection.map((b, i) => ({
        month: b.month,
        baseline: b.uss,
        intervention: result.intervention_projection[i]?.uss ?? b.uss,
      }))
    : [];

  return (
    <div>
      <Header
        title="Simulator"
        subtitle="Simulasi skenario intervensi infrastruktur terhadap USS"
      />

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Left: Parameters */}
        <div className="bg-surface rounded-lg border border-border p-5">
          <h2 className="font-display text-lg font-semibold text-text-primary mb-4">
            Skenario Intervensi
          </h2>

          {/* Kelurahan Select */}
          <div className="mb-5">
            <label className="block text-xs font-medium uppercase tracking-wider text-text-tertiary mb-1.5">
              Kelurahan
            </label>
            <select
              value={selectedKelId}
              onChange={(e) => setSelectedKelId(e.target.value)}
              className="w-full px-3 py-2.5 rounded-md border border-border bg-surface text-sm"
            >
              <option value="">Pilih kelurahan...</option>
              {ussData.map((k) => (
                <option key={k.kelurahan_id} value={k.kelurahan_id}>
                  {k.nama} (USS: {k.uss.toFixed(1)})
                </option>
              ))}
            </select>
          </div>

          {/* Sliders */}
          <div className="space-y-5">
            <SliderInput
              label="Peningkatan Drainase"
              value={drainase}
              onChange={setDrainase}
              suffix="%"
            />
            <SliderInput
              label="Perbaikan Jalan"
              value={roadRepair}
              onChange={setRoadRepair}
              suffix="%"
            />
            <SliderInput
              label="Program Sosial"
              value={socialProgram}
              onChange={setSocialProgram}
              suffix="%"
            />
          </div>

          {/* Duration Segmented Control */}
          <div className="mt-5">
            <label className="block text-xs font-medium uppercase tracking-wider text-text-tertiary mb-1.5">
              Proyeksi
            </label>
            <div className="flex gap-1 bg-bg-subtle rounded-md p-1">
              {monthOptions.map((m) => (
                <button
                  key={m}
                  onClick={() => setMonths(m)}
                  className={`flex-1 py-1.5 text-xs font-medium rounded-md transition-colors duration-100 ${
                    months === m
                      ? 'bg-surface shadow-xs text-text-primary'
                      : 'text-text-tertiary hover:text-text-secondary'
                  }`}
                >
                  {m} bln
                </button>
              ))}
            </div>
          </div>

          {error && (
            <p className="mt-3 text-xs text-zone-red">{error}</p>
          )}

          <button
            onClick={runSimulation}
            disabled={loading}
            className="w-full mt-5 py-2.5 rounded-md bg-accent text-text-inverse text-sm font-semibold hover:bg-accent-hover transition-colors duration-100 disabled:opacity-50"
          >
            {loading ? 'Menghitung proyeksi...' : 'Jalankan Simulasi'}
          </button>
        </div>

        {/* Right: Projection Chart */}
        <div className="bg-surface rounded-lg border border-border p-5">
          <h2 className="font-display text-lg font-semibold text-text-primary mb-1">
            Proyeksi USS
          </h2>
          {result && (
            <p className="text-xs text-text-secondary mb-4">
              {result.nama} · Estimasi penurunan: <span className="font-data font-bold text-zone-green">-{result.estimated_reduction.toFixed(1)} poin</span>
            </p>
          )}

          {loading ? (
            <div className="skeleton h-64 rounded-lg" />
          ) : result ? (
            <ResponsiveContainer width="100%" height={280}>
              <LineChart data={chartData} margin={{ top: 5, right: 20, left: -20, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#E8E4DC" strokeOpacity={0.3} />
                <XAxis
                  dataKey="month"
                  tick={{ fontSize: 10, fill: '#9C968F' }}
                  axisLine={false}
                  tickLine={false}
                  label={{ value: 'Bulan', position: 'insideBottom', offset: -2, fontSize: 10, fill: '#9C968F' }}
                />
                <YAxis
                  domain={[0, 100]}
                  tick={{ fontSize: 10, fill: '#9C968F' }}
                  axisLine={false}
                  tickLine={false}
                />
                <Tooltip
                  content={({ active, payload, label }) => {
                    if (!active || !payload?.length) return null;
                    return (
                      <div className="bg-surface rounded-lg shadow-md p-3 border border-border text-xs">
                        <p className="font-medium text-text-primary mb-1">Bulan {label}</p>
                        {payload.map((p) => (
                          <p key={p.dataKey as string} style={{ color: p.color }}>
                            {p.dataKey === 'baseline' ? 'Baseline' : 'Intervensi'}: {(p.value as number).toFixed(1)}
                          </p>
                        ))}
                      </div>
                    );
                  }}
                />
                <ReferenceLine y={70} stroke="#B91C1C" strokeDasharray="3 3" strokeOpacity={0.5} />
                <Line
                  type="monotone"
                  dataKey="baseline"
                  stroke="#9C968F"
                  strokeWidth={2}
                  strokeDasharray="6 3"
                  dot={false}
                  name="Baseline"
                />
                <Line
                  type="monotone"
                  dataKey="intervention"
                  stroke="#1B4F72"
                  strokeWidth={2}
                  dot={false}
                  name="Intervensi"
                />
              </LineChart>
            </ResponsiveContainer>
          ) : (
            <div className="flex items-center justify-center h-64 text-text-tertiary text-sm">
              <div className="text-center">
                <div className="text-3xl mb-2">◎</div>
                <p>Jalankan simulasi untuk melihat proyeksi</p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

function SliderInput({
  label,
  value,
  onChange,
  suffix = '',
}: {
  label: string;
  value: number;
  onChange: (v: number) => void;
  suffix?: string;
}) {
  return (
    <div>
      <div className="flex items-center justify-between mb-1.5">
        <label className="text-xs font-medium uppercase tracking-wider text-text-tertiary">
          {label}
        </label>
        <span className="font-data text-sm font-semibold text-text-primary">
          {value}{suffix}
        </span>
      </div>
      <input
        type="range"
        min={0}
        max={100}
        value={value}
        onChange={(e) => onChange(Number(e.target.value))}
        className="w-full h-1.5 rounded-full appearance-none bg-border accent-accent cursor-pointer"
      />
    </div>
  );
}
