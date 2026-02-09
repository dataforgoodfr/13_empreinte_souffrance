import { useCallback, useMemo, useState } from 'react';
import type { CageFilterValue, FilterState, MarkerStyle, Store } from './types';
import { DEFAULT_MARKER_OPACITY, DEFAULT_MARKER_SIZE, DEFAULT_SHOW_OUTLINE, DEFAULT_ZOOM_SCALE } from './types';

export function useStoreMapFilters(stores: Store[]) {
  const [cageFilter, setCageFilter] = useState<CageFilterValue>('all');
  const [selectedEnseigne, setSelectedEnseigne] = useState<string | null>(null);

  const [markerStyle, setMarkerStyle] = useState<MarkerStyle>('illustrated');
  const [markerSize, setMarkerSize] = useState(DEFAULT_MARKER_SIZE);
  const [markerOpacity, setMarkerOpacity] = useState(DEFAULT_MARKER_OPACITY);
  const [showOutline, setShowOutline] = useState(DEFAULT_SHOW_OUTLINE);
  const [zoomScale, setZoomScale] = useState(DEFAULT_ZOOM_SCALE);

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
    () => ({ cageFilter, selectedEnseigne, markerStyle, markerSize, markerOpacity, showOutline, zoomScale }),
    [cageFilter, selectedEnseigne, markerStyle, markerSize, markerOpacity, showOutline, zoomScale]
  );

  return {
    cageFilter,
    selectedEnseigne,
    markerStyle,
    markerSize,
    markerOpacity,
    showOutline,
    zoomScale,
    filterState,
    filteredStores,
    stats,
    toggleCageFilter,
    toggleEnseigne,
    setMarkerStyle,
    setMarkerSize,
    setMarkerOpacity,
    setShowOutline,
    setZoomScale,
  };
}
