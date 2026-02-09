'use client';

import { useCallback, useMemo, useState } from 'react';
import { MapContainer, TileLayer } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import clsx from 'clsx';

import { enseignes as defaultEnseignes, store as defaultStores } from '../../_data/store-data';
import type { EnseigneConfig, Store } from './types';
import { COLORS } from './types';
import { createIconPairForStyle } from './icons';
import { useStoreMapFilters } from './hooks';
import { EggMarker, MapFilterPanel, MapInitializer, MapSettingsPanel, MapZoomTracker } from './components';

type StoreMapProps = {
  stores?: Store[];
  enseignes?: EnseigneConfig[];
  heightClassName?: string;
  className?: string;
};

const REF_ZOOM = 6;

export default function StoreMap({
  stores,
  enseignes,
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
    markerOpacity,
    showOutline,
    zoomScale,
    filteredStores,
    toggleCageFilter,
    toggleEnseigne,
    setMarkerStyle,
    setMarkerSize,
    setMarkerOpacity,
    setShowOutline,
    setZoomScale,
  } = useStoreMapFilters(storeData);

  const [currentZoom, setCurrentZoom] = useState(5.5);
  const onZoomChange = useCallback((z: number) => setCurrentZoom(z), []);

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
    () => createIconPairForStyle(markerStyle, markerSize, markerOpacity, showOutline, COLORS),
    [markerStyle, markerSize, markerOpacity, showOutline]
  );

  return (
    <div
      className={clsx(
        'relative w-full overflow-hidden shadow-lg border border-gray-200/60 rounded-2xl',
        heightClassName,
        className
      )}
      style={{ '--marker-zoom-scale': zoomCssScale } as React.CSSProperties}
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
        <MapZoomTracker onZoomChange={onZoomChange} />

        <TileLayer
          url="https://{s}.tile.openstreetmap.fr/osmfr/{z}/{x}/{y}.png"
          attribution="&copy; OpenStreetMap France"
        />

        {filteredStores.map((s, i) => (
          <EggMarker
            key={`${s.category}-${i}-${markerStyle}-${markerSize}-${markerOpacity}-${showOutline}`}
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
        markerOpacity={markerOpacity}
        onChangeMarkerOpacity={setMarkerOpacity}
        showOutline={showOutline}
        onToggleOutline={setShowOutline}
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
