'use client';

import { useEffect } from 'react';
import { useMap } from 'react-leaflet';

/* Bounding box of metropolitan France (approximate). */
const FRANCE_BOUNDS: [[number, number], [number, number]] = [
  [41.3, -5.2],
  [51.1, 9.6],
];

/* smaller for mobile */
const FRANCE_BOUNDS_TIGHT: [[number, number], [number, number]] = [
  [42.3, -3.5],
  [50.5, 8.5],
];

const SMALL_SCREEN = 480;

export default function MapInitializer() {
  const map = useMap();

  useEffect(() => {
    map.invalidateSize();

    const isSmall = window.innerWidth < SMALL_SCREEN;
    const bounds = isSmall ? FRANCE_BOUNDS_TIGHT : FRANCE_BOUNDS;
    const padding: [number, number] = isSmall ? [10, 5] : [20, 20];

    map.fitBounds(bounds, { animate: false, padding, maxZoom: 18 });
  }, [map]);

  return null;
}
