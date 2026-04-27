import { useState } from 'react';
import { Header } from '../components/layout/Header';
import { AlertPanel } from '../components/dashboard/AlertPanel';
import { useAlerts } from '../hooks/useAlerts';

type FilterLevel = '' | 'watch' | 'warning' | 'emergency';

export default function Alerts() {
  const [levelFilter, setLevelFilter] = useState<FilterLevel>('');
  const [showResolved, setShowResolved] = useState(false);
  const {
    data: alerts,
    total,
    loading,
    resolveAlert,
  } = useAlerts(
    levelFilter || undefined,
    showResolved ? undefined : false
  );

  const filterButtons: { value: FilterLevel; label: string; color: string }[] = [
    { value: '', label: 'Semua', color: 'text-text-primary' },
    { value: 'emergency', label: 'Darurat', color: 'text-zone-red' },
    { value: 'warning', label: 'Peringatan', color: 'text-zone-yellow' },
    { value: 'watch', label: 'Waspada', color: 'text-zone-yellow' },
  ];

  return (
    <div>
      <Header
        title="Alert Log"
        subtitle={`${total} alert tercatat`}
      />

      {/* Filters */}
      <div className="flex items-center gap-4 mb-6">
        <div className="flex gap-1 bg-bg-subtle rounded-md p-1">
          {filterButtons.map((btn) => (
            <button
              key={btn.value}
              onClick={() => setLevelFilter(btn.value)}
              className={`px-3 py-1.5 text-xs font-medium rounded-md transition-colors duration-100 ${
                levelFilter === btn.value
                  ? 'bg-surface shadow-xs text-text-primary'
                  : 'text-text-tertiary hover:text-text-secondary'
              }`}
            >
              {btn.label}
            </button>
          ))}
        </div>

        <label className="flex items-center gap-2 text-xs text-text-secondary cursor-pointer">
          <input
            type="checkbox"
            checked={showResolved}
            onChange={(e) => setShowResolved(e.target.checked)}
            className="rounded border-border"
          />
          Tampilkan ditangani
        </label>
      </div>

      {/* Alert List */}
      <div className="max-w-2xl">
        <AlertPanel
          alerts={alerts}
          loading={loading}
          onResolve={resolveAlert}
        />
      </div>
    </div>
  );
}
