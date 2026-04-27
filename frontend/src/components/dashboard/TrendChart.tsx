import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from 'recharts';
import { formatDate } from '../../lib/formatters';
import { getZoneColor } from '../../lib/colors';
import type { USSHistoryItem } from '../../types/uss';

interface TrendChartProps {
  data: USSHistoryItem[];
  loading: boolean;
}

export function TrendChart({ data, loading }: TrendChartProps) {
  if (loading) {
    return <div className="skeleton h-48 rounded-lg" />;
  }

  if (data.length === 0) {
    return (
      <div className="flex items-center justify-center h-48 text-text-tertiary text-sm">
        Data belum tersedia
      </div>
    );
  }

  const currentUSS = data[data.length - 1]?.uss ?? 50;
  const strokeColor = getZoneColor(currentUSS);

  // Gradient color based on current zone
  const gradientId = `uss-gradient-${currentUSS >= 70 ? 'red' : currentUSS >= 40 ? 'amber' : 'green'}`;

  const chartData = data.map((item) => ({
    date: formatDate(item.computed_at),
    uss: item.uss,
    climate: item.climate_score,
    infra: item.infrastructure_score,
    soceco: item.socioeconomic_score,
  }));

  return (
    <ResponsiveContainer width="100%" height={200}>
      <AreaChart data={chartData} margin={{ top: 5, right: 10, left: -20, bottom: 0 }}>
        <defs>
          <linearGradient id={gradientId} x1="0" y1="0" x2="0" y2="1">
            <stop offset="5%" stopColor={strokeColor} stopOpacity={0.25} />
            <stop offset="95%" stopColor={strokeColor} stopOpacity={0} />
          </linearGradient>
        </defs>
        <CartesianGrid
          strokeDasharray="3 3"
          stroke="#E8E4DC"
          strokeOpacity={0.3}
          vertical={false}
        />
        <XAxis
          dataKey="date"
          tick={{ fontSize: 10, fill: '#9C968F' }}
          axisLine={false}
          tickLine={false}
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
            const d = payload[0].payload;
            return (
              <div className="bg-surface rounded-lg shadow-md p-3 border border-border text-xs">
                <p className="font-medium text-text-primary mb-1">{label}</p>
                <p className="font-data font-bold" style={{ color: getZoneColor(d.uss) }}>
                  USS: {d.uss.toFixed(1)}
                </p>
              </div>
            );
          }}
        />
        <Area
          type="monotone"
          dataKey="uss"
          stroke={strokeColor}
          strokeWidth={2}
          fill={`url(#${gradientId})`}
          dot={false}
          activeDot={{ r: 4, fill: strokeColor }}
        />
      </AreaChart>
    </ResponsiveContainer>
  );
}
