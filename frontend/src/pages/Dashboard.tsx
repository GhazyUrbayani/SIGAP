import { Header } from '../components/layout/Header';
import { ChoroplethMap } from '../components/map/ChoroplethMap';
import { USSCard } from '../components/dashboard/USSCard';
import { TrendChart } from '../components/dashboard/TrendChart';
import { AlertPanel } from '../components/dashboard/AlertPanel';
import { useUSSLatest, useUSSHistory } from '../hooks/useUSS';
import { useKelurahanGeoJSON } from '../hooks/useKelurahan';
import { useAlerts } from '../hooks/useAlerts';
import { useMapStore } from '../store/mapStore';
import { formatRelativeTime } from '../lib/formatters';
import type { USSLatestItem } from '../types/uss';

export default function Dashboard() {
  const { data: ussData, loading: ussLoading } = useUSSLatest();
  const { data: geojsonData, loading: geojsonLoading } = useKelurahanGeoJSON();
  const { data: alerts, loading: alertsLoading, resolveAlert } = useAlerts(undefined, false);
  const selectedKelurahan = useMapStore((s) => s.selectedKelurahan);
  const setSelectedKelurahan = useMapStore((s) => s.setSelectedKelurahan);
  const { data: history, loading: historyLoading } = useUSSHistory(
    selectedKelurahan?.kelurahan_id || null
  );

  const handleSelect = (item: USSLatestItem) => {
    setSelectedKelurahan(
      selectedKelurahan?.kelurahan_id === item.kelurahan_id ? null : item
    );
  };

  return (
    <div>
      <Header
        title="Dashboard"
        subtitle={
          ussData.length > 0
            ? `${ussData.length} kelurahan · Diperbarui ${formatRelativeTime(ussData[0]?.computed_at || '')}`
            : 'Memuat data...'
        }
      />

      {/* Main Grid: 60% Map / 40% Panel */}
      <div className="grid grid-cols-1 lg:grid-cols-[3fr_2fr] gap-6">
        {/* Left Column: Map + Trend */}
        <div className="space-y-5">
          <ChoroplethMap
            geojson={geojsonData}
            loading={geojsonLoading}
            selectedId={selectedKelurahan?.kelurahan_id || null}
            onSelect={handleSelect}
          />

          {/* Trend Chart (shown when kelurahan selected) */}
          {selectedKelurahan && (
            <div className="bg-surface rounded-lg border border-border p-4">
              <div className="flex items-center justify-between mb-3">
                <div>
                  <h3 className="font-display text-sm font-semibold text-text-primary">
                    Tren USS — {selectedKelurahan.nama}
                  </h3>
                  <p className="text-xs text-text-tertiary">30 hari terakhir</p>
                </div>
              </div>
              <TrendChart data={history} loading={historyLoading} />
            </div>
          )}
        </div>

        {/* Right Column: USS Cards + Alerts */}
        <div className="space-y-5">
          {/* USS Cards */}
          <div>
            <h2 className="text-xs font-medium uppercase tracking-widest text-text-tertiary mb-3">
              Skor USS per Kelurahan
            </h2>
            {ussLoading ? (
              <div className="space-y-3">
                {[1, 2, 3, 4, 5].map((i) => (
                  <div key={i} className="skeleton h-28 rounded-lg" />
                ))}
              </div>
            ) : (
              <div className="space-y-2">
                {ussData.map((item) => (
                  <USSCard
                    key={item.kelurahan_id}
                    data={item}
                    isSelected={selectedKelurahan?.kelurahan_id === item.kelurahan_id}
                    onClick={() => handleSelect(item)}
                  />
                ))}
              </div>
            )}
          </div>

          {/* Live Alerts */}
          <div>
            <h2 className="text-xs font-medium uppercase tracking-widest text-text-tertiary mb-3">
              Alert Aktif
            </h2>
            <AlertPanel
              alerts={alerts.slice(0, 5)}
              loading={alertsLoading}
              onResolve={resolveAlert}
            />
          </div>
        </div>
      </div>
    </div>
  );
}
