'use client';

import { useEffect, useState } from 'react';
import { useMap, useMapEvents } from 'react-leaflet';

type MapZoomTrackerProps = {
  // eslint-disable-next-line no-unused-vars
  onZoomChange: (zoom: number) => void;
};

export default function MapZoomTracker({ onZoomChange }: MapZoomTrackerProps) {
  const map = useMap();
  const [, setZoom] = useState(map.getZoom());

  useMapEvents({
    zoomend: () => {
      const z = map.getZoom();
      setZoom(z);
      onZoomChange(z);
    },
  });

  useEffect(() => {
    onZoomChange(map.getZoom());
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return null;
}
