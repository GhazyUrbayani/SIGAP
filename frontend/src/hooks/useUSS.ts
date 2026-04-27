import { useState, useEffect, useCallback } from 'react';
import api from '../lib/api';
import type { USSLatestItem, USSLatestResponse, USSHistoryItem } from '../types/uss';

export function useUSSLatest(kota: string = 'Bandung') {
  const [data, setData] = useState<USSLatestItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetch = useCallback(async () => {
    setLoading(true);
    try {
      const res = await api.get<USSLatestResponse>('/uss/latest', {
        params: { kota },
      });
      setData(res.data.data);
      setError(null);
    } catch (err: unknown) {
      setError('Gagal memuat data USS');
    } finally {
      setLoading(false);
    }
  }, [kota]);

  useEffect(() => {
    fetch();
    // Poll every 60 seconds
    const interval = setInterval(fetch, 60000);
    return () => clearInterval(interval);
  }, [fetch]);

  return { data, loading, error, refetch: fetch };
}

export function useUSSHistory(kelurahanId: string | null) {
  const [data, setData] = useState<USSHistoryItem[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!kelurahanId) return;
    setLoading(true);
    api
      .get(`/uss/${kelurahanId}/history`, { params: { limit: 30 } })
      .then((res) => {
        setData(res.data.history);
      })
      .catch(() => setData([]))
      .finally(() => setLoading(false));
  }, [kelurahanId]);

  return { data, loading };
}
