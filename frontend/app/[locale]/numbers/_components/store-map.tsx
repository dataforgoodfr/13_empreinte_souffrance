'use client';

import { useMemo, useState } from 'react';
import { CircleMarker, MapContainer, Popup, TileLayer } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import { store, enseignes } from '../_data/store-data';

export default function StoreMap() {
 
  const [filterCage, setFilterCage] = useState(false);
  const [filterNoCage, setFilterNoCage] = useState(false);

  // Filtres toggle : enseignes (sélection multiple)
  const [selectedEnseignes, setSelectedEnseignes] = useState<string[]>([]);

  // Handler pour toggle statut (mutuellement exclusif)
  const toggleCage = () => {
    setFilterCage(!filterCage);
    if (!filterCage) setFilterNoCage(false);
  };

  const toggleNoCage = () => {
    setFilterNoCage(!filterNoCage);
    if (!filterNoCage) setFilterCage(false);
  };

  const toggleEnseigne = (enseigneId: string) => {
    setSelectedEnseignes((prev) =>
      prev.includes(enseigneId) ? prev.filter((id) => id !== enseigneId) : [...prev, enseigneId]
    );
  };

  const filteredStores = useMemo(() => {
    return store.filter((s) => {
      if (filterCage && !s.hasCageEggs) return false;
      if (filterNoCage && s.hasCageEggs) return false;

      if (selectedEnseignes.length > 0 && !selectedEnseignes.includes(s.category)) {
        return false;
      }

      return true;
    });
  }, [filterCage, filterNoCage, selectedEnseignes]);

  return (
    <div className="relative p-section w-full h-[90dvh] md:h-[800px] overflow-hidden">
      {/* Carte Leaflet */}
      <MapContainer
        center={[46.5, 2.5]}
        zoom={6}
        scrollWheelZoom={true}
        className="w-full h-full z-0"
        minZoom={5}
        maxZoom={12}
      >
        <TileLayer url="https://{s}.tile.openstreetmap.fr/osmfr/{z}/{x}/{y}.png" />

        {/* Marqueurs */}
        {filteredStores.map((s, i) => {
          const color = s.hasCageEggs ? '#EF4444' : '#22C55E';
          const status = s.hasCageEggs ? "Présence d'œufs cage" : "Pas d'œufs cage";

          return (
            <CircleMarker
              key={`${s.category}-${i}`}
              center={s.coords}
              radius={9}
              pathOptions={{
                fillColor: color,
                fillOpacity: 1,
                color: '',
                weight: 2,
              }}
            >
              <Popup>
                <div className="min-w-[200px]">
                  <h3 className="font-bold text-lg mb-1">{s.name}</h3>
                  <p className="text-sm text-gray-600 mb-2">{s.address}</p>
                  <p className="text-sm font-semibold" style={{ color }}>
                    {status}
                  </p>
                </div>
              </Popup>
            </CircleMarker>
          );
        })}
      </MapContainer>

      {/* Encart de filtres  */}
      <div className="absolute bottom-16 left-10 z-[2] bg-white p-4 max-w-[400px] ">
        <p className="text-lg font-bold mb-1 text-gray-800 justify-self-center ">Filtres</p>

        <div className="flex flex-row">
          {/* Filtre par statut */}
          <div>
            <div className="flex flex-col justify-evenly h-full">
              <button
                onClick={toggleCage}
                title="Présence d'oeufs cage"
                className={`w-9 px-2 py-1.5 transition-all flex items-center justify-center ${
                  filterCage ? 'bg-red-200 shadow-md' : 'bg-red-50 hover:bg-red-100'
                }`}
              >
                <img alt="free egg icon" src="/logo/map_filter_icon_caged_egg.svg" />
              </button>
              <button
                onClick={toggleNoCage}
                title="Pas d'oeufs cage"
                className={`w-9 px-2 py-1.5 transition-all flex items-center justify-center ${
                  filterNoCage ? 'bg-green-200 shadow-md' : 'bg-green-50 hover:bg-green-100'
                }`}
              >
                <img alt="free egg icon" src="/logo/map_filter_icon_free_egg.svg" />
              </button>
            </div>
          </div>

          <hr className="border border-pink-3 h-[110px] items-self-center m-3" />

          {/* Filtre par enseigne */}
          <div>
            <div className="grid grid-cols-3 gap-2">

              {enseignes.map((enseigne) => {
                const isSelected = selectedEnseignes.includes(enseigne.id);
                return (
                  <button
                    key={enseigne.id}
                    onClick={() => toggleEnseigne(enseigne.id)}
                    className={`py-1.5  transition-all border-2 flex items-center justify-center gap-2 ${
                      isSelected
                        ? '  border-blue-600 shadow-md'
                        : '  border-gray-200 hover:border-blue-400 hover:bg-blue-50'
                    }`}
                    title={enseigne.name}
                  >
                    {/* Placeholder pour logo - carré coloré avec initiale */}
                    <div
                      className={`w-8 h-6 rounded flex items-center justify-center`}
                    >
                      <img alt="supermarket logo" src={enseigne.logo} />
                    </div>
                  </button>
                );
              })}
            </div>
          </div>

        </div>
      </div>
    </div>
  );
}
