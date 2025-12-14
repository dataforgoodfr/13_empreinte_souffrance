'use client';

import { useMemo, useState } from 'react';
import { CircleMarker, MapContainer, Popup, TileLayer } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import { store } from '../_data/store-data';

// Couleur + Status
const storesWithStatus = store.map((s) => {
  const hasCageEggs = Math.random() < 0.5;
  const color = hasCageEggs ? 'red' : 'green';
  const status = hasCageEggs ? "Présence d'œufs cage" : "Pas d'œufs cage";
  return { ...s, color, status };
});

// Liste des enseignes distinctes pour le select
const enseignes = Array.from(new Set(storesWithStatus.map((s) => s.category)));

export default function StoreMap() {
  const [selectedEnseigne, setSelectedEnseigne] = useState<'all' | string>('all');
  const [selectedStatus, setSelectedStatus] = useState<'all' | 'cage' | 'nocage'>('all');

  const filteredStores = useMemo(() => {
    return storesWithStatus.filter((s) => {
      if (selectedEnseigne !== 'all' && s.category !== selectedEnseigne) return false;
      if (selectedStatus === 'cage' && s.status !== "Présence d'œufs cage") return false;
      if (selectedStatus === 'nocage' && s.status !== "Pas d'œufs cage") return false;
      return true;
    });
  }, [selectedEnseigne, selectedStatus]);

  return (
    <div className="flex flex-col gap-4 h-[50vh]">
      {/* Filtres & légendes */}
      <fieldset className="flex flex-wrap md:flex-row justify-start md:justify-center items-center gap-4">

        <div className="flex flex-col gap-1">
          <label className="font-bold">Enseigne</label>
          <select
            value={selectedEnseigne}
            onChange={(e) => setSelectedEnseigne(e.target.value)}
            className="border rounded px-2 py-1 text-sm"
          >
            <option value="all">Toutes les enseignes</option>
            {enseignes.map((e) => (
              <option key={e} value={e}>
                {e.charAt(0).toUpperCase() + e.slice(1)}
              </option>
            ))}
          </select>
        </div>

        <div className="flex flex-col gap-1">
          <label className="font-bold">Présence d'oeuf</label>
          <select
            value={selectedStatus}
            onChange={(e) =>
              setSelectedStatus(e.target.value as 'all' | 'cage' | 'nocage')
            }
            className="border rounded px-2 py-1 text-sm"
          >
            <option value="all">Tous les magasins</option>
            <option value="cage">Présence d'œufs cage</option>
            <option value="nocage">Pas d'œufs cage</option>
          </select>
        </div>

        {/* Légende */}
        <div className="flex flex-col gap-1 ">
          <p className="font-bold">Légende</p>
          <div className="flex items-center gap-2">
            <span className="inline-block w-3 h-3 rounded-full bg-red-500" />
            <p>Présence d'œufs cage</p>
          </div>
          <div className="flex items-center gap-2">
            <span className="inline-block w-3 h-3 rounded-full bg-green-500" />
            <p>Pas d'œufs cage</p>
          </div>
        </div>
      </fieldset>

      {/* Carte */}
      <div
        className="
          w-full
          max-w-[90vw]
          h-[70vh]
          md:h-[60vh]
        "
      >
        <MapContainer
          center={[46.5, 2.5]}
          zoom={5}
          scrollWheelZoom={false}
          className="w-full h-full"
          minZoom={5}
          maxZoom={10}
          maxBounds={[
            [51.5, -5.5],
            [41, 9.8],
          ]}
          maxBoundsViscosity={1.0}
        >
          <TileLayer
            url="https://{s}.tile.openstreetmap.fr/osmfr/{z}/{x}/{y}.png"
            attribution="&copy; OpenStreetMap France, contributeurs OpenStreetMap"
          />

          {filteredStores.map((s, i) => (
            <CircleMarker
              key={i}
              center={s.coords}
              radius={8}
              pathOptions={{
                fillColor: s.color,
                fillOpacity: 1,
                color: 'none',
                weight: 2,
              }}
            >
              <Popup>
                <div>
                  <h3>{s.name}</h3>
                  <p>{s.address}</p>
                  <p>{s.status}</p>
                </div>
              </Popup>
            </CircleMarker>
          ))}
        </MapContainer>
      </div>
    </div>
  );
}
