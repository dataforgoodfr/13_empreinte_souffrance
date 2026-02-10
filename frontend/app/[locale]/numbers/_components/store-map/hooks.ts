import { useCallback, useMemo, useState } from 'react';
import type { CageFilterValue, FilterState, MarkerStyle, OutlineMode, Store } from './types';
import { DEFAULT_MARKER_SIZE, DEFAULT_OUTLINE_MODE, DEFAULT_STROKE_WIDTH, DEFAULT_ZOOM_SCALE } from './types';

type InitialSettings = {
  style?: MarkerStyle;
  size?: number;
  outlineMode?: OutlineMode;
  strokeWidth?: number;
  zoomScale?: number;
};

export function useStoreMapFilters(stores: Store[], initial?: InitialSettings) {
  const [cageFilter, setCageFilter] = useState<CageFilterValue>('all');
  const [selectedEnseigne, setSelectedEnseigne] = useState<string | null>(null);

  const [markerStyle, setMarkerStyle] = useState<MarkerStyle>(initial?.style ?? 'illustrated');
  const [markerSize, setMarkerSize] = useState(initial?.size ?? DEFAULT_MARKER_SIZE);
  const [outlineMode, setOutlineMode] = useState<OutlineMode>(initial?.outlineMode ?? DEFAULT_OUTLINE_MODE);
  const [strokeWidth, setStrokeWidth] = useState(initial?.strokeWidth ?? DEFAULT_STROKE_WIDTH);
  const [zoomScale, setZoomScale] = useState(initial?.zoomScale ?? DEFAULT_ZOOM_SCALE);

  const toggleCageFilter = useCallback((value: CageFilterValue) => {
    setCageFilter((prev) => (prev === value ? 'all' : value));
  }, []);

  const toggleEnseigne = useCallback((enseigneId: string) => {
    setSelectedEnseigne((prev) => (prev === enseigneId ? null : enseigneId));
  }, []);

  const filteredStores = useMemo(() => {
    return stores.filter((s) => {
      if (cageFilter === 'cage' && !s.hasCageEggs) return false;
      if (cageFilter === 'noCage' && s.hasCageEggs) return false;
      if (selectedEnseigne && s.category !== selectedEnseigne) return false;
      return true;
    });
  }, [stores, cageFilter, selectedEnseigne]);

  const stats = useMemo(() => {
    const pool = selectedEnseigne ? stores.filter((s) => s.category === selectedEnseigne) : stores;
    return {
      total: pool.length,
      withCage: pool.filter((s) => s.hasCageEggs).length,
    };
  }, [stores, selectedEnseigne]);

  const filterState: FilterState = useMemo(
    () => ({ cageFilter, selectedEnseigne, markerStyle, markerSize, outlineMode, strokeWidth, zoomScale }),
    [cageFilter, selectedEnseigne, markerStyle, markerSize, outlineMode, strokeWidth, zoomScale]
  );

  return {
    cageFilter,
    selectedEnseigne,
    markerStyle,
    markerSize,
    outlineMode,
    strokeWidth,
    zoomScale,
    filterState,
    filteredStores,
    stats,
    toggleCageFilter,
    toggleEnseigne,
    setMarkerStyle,
    setMarkerSize,
    setOutlineMode,
    setStrokeWidth,
    setZoomScale,
  };
}
