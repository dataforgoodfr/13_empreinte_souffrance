'use client';

import { Marker, Popup } from 'react-leaflet';
import type { DivIcon } from 'leaflet';
import type { MapColors, Store } from '../types';
import { COLORS } from '../types';
import MapPopup from './MapPopup';

type EggMarkerProps = {
  store: Store;
  cageIcon: DivIcon;
  freeIcon: DivIcon;
  colors?: MapColors;
};

export default function EggMarker({ store, cageIcon, freeIcon, colors = COLORS }: EggMarkerProps) {
  return (
    <Marker position={store.coords} icon={store.hasCageEggs ? cageIcon : freeIcon}>
      <Popup>
        <MapPopup store={store} colors={colors} />
      </Popup>
    </Marker>
  );
}
