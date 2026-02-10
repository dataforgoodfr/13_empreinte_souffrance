'use client';

import { useCallback, useMemo, useRef, useState } from 'react';
import { MapContainer, TileLayer } from 'react-leaflet';
import type { LatLngBounds } from 'leaflet';
import 'leaflet/dist/leaflet.css';
import clsx from 'clsx';

import { enseignes as defaultEnseignes, store as defaultStores } from '../../_data/store-data';
import type { EnseigneConfig, MarkerStyle, OutlineMode, Store } from './types';
import { COLORS } from './types';
import { createIconPairForStyle } from './icons';
import { useStoreMapFilters } from './hooks';
import { EggMarker, MapFilterPanel, MapInitializer, MapSettingsPanel, MapZoomTracker } from './components';

type StoreMapProps = {
  stores?: Store[];
  enseignes?: EnseigneConfig[];
  /** Override the initial marker style (default: 'illustrated'). */
  initialStyle?: MarkerStyle;
  /** Override the initial marker size in px (default: 30). */
  initialSize?: number;
  /** Override the initial outline mode: 'none' | 'stroke' | 'shadow' (default: 'none'). */
  initialOutlineMode?: OutlineMode;
  /** Override the initial zoom-adaptive scale 0–1 (default: 0.25). */
  initialZoomScale?: number;
  heightClassName?: string;
  className?: string;
};

const REF_ZOOM = 6;

export default function StoreMap({
  stores,
  enseignes,
  initialStyle,
  initialSize,
  initialOutlineMode,
  initialZoomScale,
  heightClassName = 'h-[85dvh] md:h-[560px]',
  className,
}: StoreMapProps) {
  const storeData = stores ?? defaultStores;
  const enseigneData = enseignes ?? defaultEnseignes;

  const {
    cageFilter,
    selectedEnseigne,
    markerStyle,
    markerSize,
    outlineMode,
    strokeWidth,
    zoomScale,
    filteredStores,
    toggleCageFilter,
    toggleEnseigne,
    setMarkerStyle,
    setMarkerSize,
    setOutlineMode,
    setStrokeWidth,
    setZoomScale,
  } = useStoreMapFilters(storeData, {
    style: initialStyle,
    size: initialSize,
    outlineMode: initialOutlineMode,
    zoomScale: initialZoomScale,
  });

  const [currentZoom, setCurrentZoom] = useState(5.5);
  const onZoomChange = useCallback((z: number) => setCurrentZoom(z), []);

  /* ── Bounds-based culling — only render markers visible on screen ───── */
  const boundsRef = useRef<LatLngBounds | null>(null);
  const [boundsVersion, setBoundsVersion] = useState(0);
  const onBoundsChange = useCallback((b: LatLngBounds) => {
    boundsRef.current = b;
    setBoundsVersion((v) => v + 1);
  }, []);

  const visibleStores = useMemo(() => {
    const bounds = boundsRef.current;
    if (!bounds) return filteredStores;
    // Pad bounds ~10% so markers near the edge don't pop in/out abruptly
    const padded = bounds.pad(0.1);
    return filteredStores.filter((s) => padded.contains(s.coords));
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [filteredStores, boundsVersion]);

  /*
   * CSS scale factor applied via `--marker-zoom-scale` custom property.
   * Icons stay at the base size; the visual scaling is done purely in CSS
   * with a smooth transition — no icon recreation needed.
   */
  const zoomCssScale = useMemo(() => {
    if (zoomScale === 0) return 1;
    const factor = Math.pow(2, (currentZoom - REF_ZOOM) * zoomScale * 0.2);
    return Math.max(0.3, Math.min(2.5, factor));
  }, [currentZoom, zoomScale]);

  const icons = useMemo(
    () => createIconPairForStyle(markerStyle, markerSize, outlineMode, COLORS, strokeWidth),
    [markerStyle, markerSize, outlineMode, strokeWidth]
  );

  return (
    <div
      className={clsx(
        'relative w-full overflow-hidden shadow-lg border border-gray-200/60 rounded-2xl',
        heightClassName,
        className
      )}
      style={{ '--marker-zoom-scale': zoomCssScale, '--marker-stroke-w': `${strokeWidth}px` } as React.CSSProperties}
    >
      <MapContainer
        center={[46.8, 2.5]}
        zoom={5.5}
        scrollWheelZoom={true}
        className="w-full h-full z-0"
        minZoom={4}
        maxZoom={18}
      >
        <MapInitializer />
        <MapZoomTracker onZoomChange={onZoomChange} onBoundsChange={onBoundsChange} />

        <TileLayer
          url="https://{s}.tile.openstreetmap.fr/osmfr/{z}/{x}/{y}.png"
          attribution="&copy; OpenStreetMap France"
        />

        {visibleStores.map((s, i) => (
          <EggMarker
            key={`${s.category}-${i}-${markerStyle}-${markerSize}-${outlineMode}-${strokeWidth}`}
            store={s}
            cageIcon={icons.cage}
            freeIcon={icons.free}
          />
        ))}
      </MapContainer>

      <MapSettingsPanel
        currentStyle={markerStyle}
        onChangeStyle={setMarkerStyle}
        markerSize={markerSize}
        onChangeMarkerSize={setMarkerSize}
        outlineMode={outlineMode}
        onChangeOutlineMode={setOutlineMode}
        strokeWidth={strokeWidth}
        onChangeStrokeWidth={setStrokeWidth}
        zoomScale={zoomScale}
        onChangeZoomScale={setZoomScale}
      />

      <MapFilterPanel
        cageFilter={cageFilter}
        selectedEnseigne={selectedEnseigne}
        enseigneList={enseigneData}
        onToggleCage={toggleCageFilter}
        onToggleEnseigne={toggleEnseigne}
      />
    </div>
  );
}
