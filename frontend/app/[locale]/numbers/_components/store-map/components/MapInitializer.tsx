'use client';

import { useEffect } from 'react';
import { useMap } from 'react-leaflet';

/* Centre of metropolitan France. */
const FRANCE_CENTER: [number, number] = [46.6, 2.5];

const SMALL_SCREEN = 480;
const DESKTOP_ZOOM = 5.7;
const MOBILE_ZOOM = 6;

export default function MapInitializer() {
  const map = useMap();

  useEffect(() => {
    map.invalidateSize();

    const zoom = window.innerWidth < SMALL_SCREEN ? MOBILE_ZOOM : DESKTOP_ZOOM;
    map.setView(FRANCE_CENTER, zoom, { animate: false });
  }, [map]);

  return null;
}
