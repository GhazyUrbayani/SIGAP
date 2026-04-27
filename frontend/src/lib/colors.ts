/**
 * Get zone color based on USS score.
 * GREEN: 0-39, YELLOW: 40-69, RED: 70-100
 */
export function getZoneColor(score: number | null): string {
  if (score === null) return '#9C968F';
  if (score < 40) return '#1A7A4A';
  if (score < 70) return '#B45309';
  return '#B91C1C';
}

export function getZoneBgColor(score: number | null): string {
  if (score === null) return '#F7F6F3';
  if (score < 40) return '#EBFAF3';
  if (score < 70) return '#FFF8EB';
  return '#FFF1F0';
}

export function getZoneLabel(score: number | null): string {
  if (score === null) return 'N/A';
  if (score < 40) return 'HIJAU';
  if (score < 70) return 'KUNING';
  return 'MERAH';
}

export function getZoneLevelLabel(level: string | null): string {
  switch (level) {
    case 'very_low': return 'Sangat Rendah';
    case 'low': return 'Rendah';
    case 'medium': return 'Sedang';
    case 'high': return 'Tinggi';
    case 'very_high': return 'Sangat Tinggi';
    default: return '-';
  }
}
