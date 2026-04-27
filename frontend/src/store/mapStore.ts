import { create } from 'zustand';
import type { USSLatestItem } from '../types/uss';

interface MapState {
  selectedKelurahan: USSLatestItem | null;
  setSelectedKelurahan: (kel: USSLatestItem | null) => void;
}

export const useMapStore = create<MapState>((set) => ({
  selectedKelurahan: null,
  setSelectedKelurahan: (kel) => set({ selectedKelurahan: kel }),
}));
