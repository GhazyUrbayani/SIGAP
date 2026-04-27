import { useState, useEffect, useCallback } from 'react';
import api from '../lib/api';
import type { AlertItem, AlertListResponse } from '../types/auth';

export function useAlerts(level?: string, isResolved?: boolean) {
  const [data, setData] = useState<AlertItem[]>([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetch = useCallback(async () => {
    setLoading(true);
    try {
      const params: Record<string, unknown> = {};
      if (level) params.level = level;
      if (isResolved !== undefined) params.is_resolved = isResolved;
      const res = await api.get<AlertListResponse>('/alerts', { params });
      setData(res.data.data);
      setTotal(res.data.total);
      setError(null);
    } catch {
      setError('Gagal memuat data alert');
    } finally {
      setLoading(false);
    }
  }, [level, isResolved]);

  useEffect(() => {
    fetch();
  }, [fetch]);

  const resolveAlert = async (alertId: string) => {
    try {
      await api.patch(`/alerts/${alertId}/resolve`);
      await fetch();
    } catch {
      setError('Gagal menandai alert');
    }
  };

  return { data, total, loading, error, refetch: fetch, resolveAlert };
}
