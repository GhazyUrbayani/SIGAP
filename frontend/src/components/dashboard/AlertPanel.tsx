import { formatRelativeTime } from '../../lib/formatters';
import type { AlertItem } from '../../types/auth';

interface AlertPanelProps {
  alerts: AlertItem[];
  loading: boolean;
  onResolve?: (id: string) => void;
}

export function AlertPanel({ alerts, loading, onResolve }: AlertPanelProps) {
  if (loading) {
    return (
      <div className="space-y-3">
        {[1, 2, 3].map((i) => (
          <div key={i} className="skeleton h-24 rounded-lg" />
        ))}
      </div>
    );
  }

  if (alerts.length === 0) {
    return (
      <div className="text-center py-12 text-text-tertiary">
        <div className="text-3xl mb-2">✓</div>
        <p className="text-sm font-medium text-zone-green">
          Semua kelurahan dalam zona aman
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-3">
      {alerts.map((alert) => (
        <AlertCard
          key={alert.id}
          alert={alert}
          onResolve={onResolve}
        />
      ))}
    </div>
  );
}

function AlertCard({
  alert,
  onResolve,
}: {
  alert: AlertItem;
  onResolve?: (id: string) => void;
}) {
  const levelColors: Record<string, { bg: string; border: string; label: string }> = {
    watch: { bg: '#FFF8EB', border: '#B45309', label: 'WASPADA' },
    warning: { bg: '#FFF8EB', border: '#B45309', label: 'PERINGATAN' },
    emergency: { bg: '#FFF1F0', border: '#B91C1C', label: 'DARURAT' },
  };

  const style = levelColors[alert.trigger_level] || levelColors.watch;

  return (
    <div
      className={`rounded-lg p-4 border-l-[3px] ${
        alert.is_resolved ? 'opacity-50' : ''
      }`}
      style={{
        backgroundColor: style.bg,
        borderLeftColor: style.border,
      }}
      aria-live="polite"
    >
      <div className="flex items-center justify-between mb-2">
        <span
          className="text-xs font-semibold uppercase tracking-wider"
          style={{ color: style.border }}
        >
          ● {style.label} · {formatRelativeTime(alert.created_at)}
        </span>
      </div>

      <p className="text-sm font-semibold text-text-primary mb-1">
        {alert.kelurahan_nama || 'Kelurahan'} — USS {alert.uss_value}
      </p>

      <p className="text-sm text-text-secondary leading-relaxed mb-3">
        {alert.message.slice(alert.message.indexOf('—') + 2, 200)}
        {alert.message.length > 200 ? '...' : ''}
      </p>

      {!alert.is_resolved && onResolve && (
        <div className="flex gap-2">
          <button
            onClick={() => onResolve(alert.id)}
            className="text-xs font-medium px-3 py-1.5 rounded-md bg-accent text-text-inverse hover:bg-accent-hover transition-colors duration-100"
          >
            Tandai Ditangani
          </button>
        </div>
      )}
    </div>
  );
}
