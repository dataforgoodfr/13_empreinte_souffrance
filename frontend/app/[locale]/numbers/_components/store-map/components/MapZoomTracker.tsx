'use client';

import { useEffect, useState } from 'react';
import { useMap, useMapEvents } from 'react-leaflet';
import type { LatLngBounds } from 'leaflet';

type MapZoomTrackerProps = {
  // eslint-disable-next-line no-unused-vars
  onZoomChange: (zoom: number) => void;
  // eslint-disable-next-line no-unused-vars
  onBoundsChange?: (bounds: LatLngBounds) => void;
};

export default function MapZoomTracker({ onZoomChange, onBoundsChange }: MapZoomTrackerProps) {
  const map = useMap();
  const [, setZoom] = useState(map.getZoom());

  useMapEvents({
    zoomend: () => {
      const z = map.getZoom();
      setZoom(z);
      onZoomChange(z);
      onBoundsChange?.(map.getBounds());
    },
    moveend: () => {
      onBoundsChange?.(map.getBounds());
    },
  });

  /* Report initial values on mount */
  useEffect(() => {
    onZoomChange(map.getZoom());
    onBoundsChange?.(map.getBounds());
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return null;
}
