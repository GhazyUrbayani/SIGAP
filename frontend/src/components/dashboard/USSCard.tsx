import { getZoneColor, getZoneBgColor, getZoneLabel } from '../../lib/colors';
import { formatUSS } from '../../lib/formatters';
import type { USSLatestItem } from '../../types/uss';

interface USSCardProps {
  data: USSLatestItem;
  isSelected?: boolean;
  onClick?: () => void;
  previousUss?: number | null;
}

export function USSCard({ data, isSelected, onClick, previousUss }: USSCardProps) {
  const zoneColor = getZoneColor(data.uss);
  const zoneBg = getZoneBgColor(data.uss);
  const zoneLabel = getZoneLabel(data.uss);
  const isCritical = data.uss >= 85;
  const delta = previousUss !== null && previousUss !== undefined
    ? data.uss - previousUss
    : null;

  return (
    <button
      onClick={onClick}
      className={`
        w-full text-left rounded-lg p-4 transition-colors duration-200
        border-l-[3px] cursor-pointer
        ${isCritical ? 'zone-pulse-critical' : ''}
        ${isSelected ? 'shadow-md' : 'shadow-xs hover:shadow-sm'}
      `}
      style={{
        borderLeftColor: zoneColor,
        backgroundColor: isSelected ? zoneBg : '#FFFFFF',
      }}
      aria-label={`Urban Stress Score ${data.uss} dari 100, zona ${zoneLabel}`}
    >
      {/* Header */}
      <div className="flex items-center justify-between mb-2">
        <span className="text-sm font-medium text-text-primary uppercase tracking-wide">
          {data.nama}
        </span>
        <span
          className="text-xs font-semibold uppercase px-2 py-0.5 rounded-sm"
          style={{ color: zoneColor, backgroundColor: zoneBg }}
          role="status"
        >
          ● {zoneLabel}
        </span>
      </div>

      {/* USS Score */}
      <div className="flex items-baseline gap-2 mb-3">
        <span
          className="font-data text-3xl font-black animate-count-up"
          style={{ color: zoneColor }}
        >
          {formatUSS(data.uss)}
        </span>
        {delta !== null && (
          <span
            className={`text-xs font-medium ${
              delta > 0 ? 'text-zone-red' : delta < 0 ? 'text-zone-green' : 'text-text-tertiary'
            }`}
          >
            {delta > 0 ? '↑' : delta < 0 ? '↓' : '—'} {Math.abs(delta).toFixed(1)}
          </span>
        )}
      </div>

      {/* Dimension Bars */}
      <div className="space-y-1.5">
        <DimensionBar label="Iklim" value={data.climate_score} tooltip="Kondisi Lingkungan (Suhu, Vegetasi, dll)" />
        <DimensionBar label="Infra" value={data.infrastructure_score} tooltip="Infrastruktur (Kerapatan Bangunan, Jalan, dll)" />
        <DimensionBar label="Sosek" value={data.socioeconomic_score} tooltip="Sosial Ekonomi (Kepadatan Penduduk, Aktivitas, dll)" />
      </div>
    </button>
  );
}

function DimensionBar({ label, value, tooltip }: { label: string; value: number; tooltip?: string }) {
  const color = getZoneColor(value);
  return (
    <div className="flex items-center gap-2">
      <div className="relative flex items-center group">
        <span 
          className={`text-xs text-text-tertiary w-8 font-medium ${tooltip ? 'cursor-help decoration-dotted underline decoration-text-tertiary/50 underline-offset-2' : ''}`}
        >
          {label}
        </span>
        {tooltip && (
          <div className="absolute left-0 bottom-full mb-1 hidden group-hover:block w-40 z-50 pointer-events-none">
            <div className="bg-gray-800 text-white text-[10px] rounded py-1 px-1.5 shadow-lg leading-relaxed whitespace-normal text-left font-normal normal-case">
              {tooltip}
              <div className="absolute -bottom-1 left-3 w-2 h-2 bg-gray-800 transform rotate-45"></div>
            </div>
          </div>
        )}
      </div>
      <div className="flex-1 h-1.5 bg-border rounded-full overflow-hidden">
        <div
          className="h-full rounded-full transition-all duration-200"
          style={{
            width: `${Math.min(100, value)}%`,
            backgroundColor: color,
          }}
        />
      </div>
      <span className="font-data text-xs text-text-secondary w-7 text-right">
        {value.toFixed(0)}
      </span>
    </div>
  );
}
