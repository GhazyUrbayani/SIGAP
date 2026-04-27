/**
 * Format USS score for display.
 */
export function formatUSS(score: number | null): string {
  if (score === null) return '—';
  return score.toFixed(1);
}

/**
 * Format delta with direction arrow.
 */
export function formatDelta(delta: number): string {
  if (delta > 0) return `↑ ${delta.toFixed(1)}`;
  if (delta < 0) return `↓ ${Math.abs(delta).toFixed(1)}`;
  return '— 0.0';
}

/**
 * Format date for display (DD MMM format).
 */
export function formatDate(dateStr: string): string {
  const date = new Date(dateStr);
  const months = [
    'Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun',
    'Jul', 'Ags', 'Sep', 'Okt', 'Nov', 'Des',
  ];
  return `${date.getDate()} ${months[date.getMonth()]}`;
}

/**
 * Format relative time (e.g. "14 menit lalu").
 */
export function formatRelativeTime(dateStr: string): string {
  const diff = Date.now() - new Date(dateStr).getTime();
  const minutes = Math.floor(diff / 60000);
  if (minutes < 1) return 'Baru saja';
  if (minutes < 60) return `${minutes} menit lalu`;
  const hours = Math.floor(minutes / 60);
  if (hours < 24) return `${hours} jam lalu`;
  const days = Math.floor(hours / 24);
  return `${days} hari lalu`;
}
