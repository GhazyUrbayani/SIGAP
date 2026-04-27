import { getZoneColor, getZoneBgColor, getZoneLabel } from '../../lib/colors';
import type { USSLatestItem } from '../../types/uss';

interface ChoroplethMapProps {
  data: USSLatestItem[];
  selectedId: string | null;
  onSelect: (item: USSLatestItem) => void;
}

/**
 * Choropleth map visualization.
 *
 * NOTE: This is a simplified SVG-based map representation for the prototype.
 * In production, this would use Azure Maps SDK with real GeoJSON boundaries.
 * The component renders an interactive grid of kelurahan zones with
 * USS-based color coding matching the UIUX specification.
 */
export function ChoroplethMap({ data, selectedId, onSelect }: ChoroplethMapProps) {
  if (data.length === 0) {
    return (
      <div className="skeleton h-[400px] rounded-lg" />
    );
  }

  return (
    <div className="relative bg-surface rounded-lg border border-border overflow-hidden">
      {/* Map Header */}
      <div className="absolute top-3 left-3 z-10 bg-surface/90 backdrop-blur-sm rounded-md px-3 py-2 shadow-sm border border-border">
        <p className="font-display text-xs font-semibold text-text-primary uppercase tracking-wider">
          Peta Kerentanan Urban
        </p>
        <p className="text-xs text-text-tertiary">Kota Bandung</p>
      </div>

      {/* Simplified Map Grid */}
      <div className="p-8 pt-16">
        <svg viewBox="0 0 500 400" className="w-full h-[360px]">
          {/* Background - city outline */}
          <rect
            x="20" y="20" width="460" height="360"
            rx="8" fill="#EFEDE8" stroke="#E8E4DC" strokeWidth="1"
          />

          {/* Kelurahan polygons - positioned to approximate Bandung layout */}
          {data.map((item, i) => {
            const positions = [
              { x: 80, y: 60, w: 160, h: 140 },   // Sukasari (NW)
              { x: 250, y: 50, w: 180, h: 130 },   // Cibeunying Kidul (NE)
              { x: 50, y: 200, w: 170, h: 150 },    // Cicendo (SW)
              { x: 230, y: 190, w: 140, h: 130 },   // Coblong (Center)
              { x: 280, y: 220, w: 170, h: 140 },   // Bandung Wetan (SE)
            ];
            const pos = positions[i % positions.length];
            const color = getZoneColor(item.uss);
            const isSelected = selectedId === item.kelurahan_id;
            const isCritical = item.uss >= 85;
            const opacity = isSelected ? 0.85 : 0.55;

            return (
              <g key={item.kelurahan_id} className="cursor-pointer">
                <rect
                  x={pos.x}
                  y={pos.y}
                  width={pos.w}
                  height={pos.h}
                  rx="6"
                  fill={color}
                  fillOpacity={opacity}
                  stroke={isSelected ? color : '#C9C4B8'}
                  strokeWidth={isSelected ? 3 : 1}
                  onClick={() => onSelect(item)}
                  className={`transition-opacity duration-200 hover:fill-opacity-[0.85] ${
                    isCritical ? 'zone-pulse-critical' : ''
                  }`}
                />
                {/* Kelurahan label */}
                <text
                  x={pos.x + pos.w / 2}
                  y={pos.y + pos.h / 2 - 8}
                  textAnchor="middle"
                  className="fill-white font-body text-xs font-semibold pointer-events-none"
                  style={{ fontSize: '11px' }}
                >
                  {item.nama}
                </text>
                {/* USS value */}
                <text
                  x={pos.x + pos.w / 2}
                  y={pos.y + pos.h / 2 + 12}
                  textAnchor="middle"
                  className="fill-white font-data font-bold pointer-events-none"
                  style={{ fontSize: '16px' }}
                >
                  {item.uss.toFixed(1)}
                </text>
              </g>
            );
          })}
        </svg>
      </div>

      {/* Legend */}
      <div className="absolute bottom-3 right-3 bg-surface/90 backdrop-blur-sm rounded-md px-3 py-2 shadow-sm border border-border">
        <div className="flex items-center gap-3 text-xs">
          <span className="flex items-center gap-1">
            <span className="w-3 h-3 rounded-sm bg-zone-green opacity-60" />
            <span className="text-text-secondary">0–39</span>
          </span>
          <span className="flex items-center gap-1">
            <span className="w-3 h-3 rounded-sm bg-zone-yellow opacity-60" />
            <span className="text-text-secondary">40–69</span>
          </span>
          <span className="flex items-center gap-1">
            <span className="w-3 h-3 rounded-sm bg-zone-red opacity-70" />
            <span className="text-text-secondary">70–100</span>
          </span>
        </div>
      </div>
    </div>
  );
}
