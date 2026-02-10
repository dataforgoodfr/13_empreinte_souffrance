import type { EnseigneConfig } from '../../_data/store-data';

export type Store = {
  name: string;
  coords: [number, number];
  category: string;
  address: string;
  hasCageEggs: boolean;
  nbRef: number;
  urlImg: string | null;
};

export type { EnseigneConfig };

export type CageFilterValue = 'all' | 'cage' | 'noCage';

export type MarkerStyle = 'circle' | 'illustrated' | 'illustrated-noborder' | 'illustrated-mixed';

export type FilterState = {
  cageFilter: CageFilterValue;
  selectedEnseigne: string | null;
  markerStyle: MarkerStyle;
  markerSize: number;
  showOutline: boolean;
  zoomScale: number;
};

export type MapColors = {
  cage: string;
  cageStroke: string;
  noCage: string;
  noCageStroke: string;
};

export const COLORS: MapColors = {
  cage: '#ff584b',
  cageStroke: '#d43d30',
  noCage: '#22C55E',
  noCageStroke: '#1a9e48',
};

export const DEFAULT_MARKER_SIZE = 27;
export const DEFAULT_SHOW_OUTLINE = false;
export const DEFAULT_ZOOM_SCALE = 0.25;
