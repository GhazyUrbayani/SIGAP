import { useState, useEffect, useCallback } from 'react';
import api from '../lib/api';
import type { KelurahanGeoJSON } from '../types/kelurahan';

export function useKelurahanGeoJSON(kota: string = 'Bandung') {
  const [data, setData] = useState<KelurahanGeoJSON | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchGeoJSON = useCallback(async () => {
    setLoading(true);
    try {
      const res = await api.get<KelurahanGeoJSON>('/kelurahan/geojson', {
        params: { kota },
      });
      setData(res.data);
      setError(null);
    } catch (err: unknown) {
      setError('Gagal memuat peta kerentanan');
    } finally {
      setLoading(false);
    }
  }, [kota]);

  useEffect(() => {
    fetchGeoJSON();
  }, [fetchGeoJSON]);

  return { data, loading, error, refetch: fetchGeoJSON };
}
