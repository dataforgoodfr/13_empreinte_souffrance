'use client';

import { useMemo, useState } from 'react';
import { CircleMarker, MapContainer, Popup, TileLayer } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import { store, enseignes } from '../_data/store-data';

export default function StoreMap() {
  // Filtres toggle : statut (mutuellement exclusif)
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
    setSelectedEnseignes(prev =>
      prev.includes(enseigneId)
        ? prev.filter(id => id !== enseigneId)
        : [...prev, enseigneId] 
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
        <TileLayer
          url="https://{s}.tile.openstreetmap.fr/osmfr/{z}/{x}/{y}.png"
        
        />

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
                fillOpacity: 0.9,
                color: '#FFFFFF',
                weight: 2,
              }}
            >
              <Popup>
                <div className="min-w-[200px]">
                  <h3 className="font-bold text-lg mb-1">{s.name}</h3>
                  <p className="text-sm text-gray-600 mb-2">{s.address}</p>
                  <p 
                    className="text-sm font-semibold"
                    style={{ color }}
                  >
                    {status}
                  </p>
                </div>
              </Popup>
            </CircleMarker>
          );
        })}
      </MapContainer>

      {/* Encart de filtres - overlay sur la carte */}
      <div className="absolute bottom-14 right-6 z-[2] bg-white p-6 max-w-[200px] ">
        <p className="text-lg font-bold mb-4 text-gray-800">Filtres</p>
        

        {/* Filtre par statut */}
        <div className="">
          <div className="space-y-2">
            <button
              onClick={toggleCage}
              className={`w-full px-4 py-2.5 rounded-lg text-caption font-medium transition-all flex items-center justify-center ${
                filterCage
                  ? 'bg-red-500 text-white'
                  : 'bg-red-50 text-red-700 hover:bg-red-100'
              }`}
            >
              <span>Présence d'œufs cage</span>
              
            </button>
            <button
              onClick={toggleNoCage}
              className={`w-full px-4 py-2.5 rounded-lg text-caption font-medium transition-all flex items-center justify-center ${
                filterNoCage
                  ? 'bg-green-600 text-white shadow-md'
                  : 'bg-green-50 text-green-700 hover:bg-green-100'
              }`}
            >
              <span>Pas d'œufs cage</span>
            </button>
          </div>
        </div>

        <hr className='border border-pink-3 w-1/2 justify-self-center m-3'/>

        {/* Filtre par enseigne */}
        <div>
          <div className="grid grid-cols-2 gap-2">
            {/* Boutons enseignes avec sélection multiple */}
            {enseignes.map((enseigne) => {
              const isSelected = selectedEnseignes.includes(enseigne.id);
              return (
                <button
                  key={enseigne.id}
                  onClick={() => toggleEnseigne(enseigne.id)}
                  className={`px-3 py-2.5 rounded-lg text-xs font-medium transition-all border-2 flex items-center justify-center gap-2 ${
                    isSelected
                      ? 'bg-blue-500 text-white border-blue-600 shadow-md'
                      : 'bg-white text-gray-700 border-gray-200 hover:border-blue-400 hover:bg-blue-50'
                  }`}
                  title={enseigne.name}
                >
                  {/* Placeholder pour logo - carré coloré avec initiale */}
                  <div className={`w-6 h-6 rounded flex items-center justify-center text-xs font-bold ${
                    isSelected ? 'bg-white/20' : 'bg-gray-200'
                  }`}>
                    {enseigne.name.charAt(0)}
                  </div>
                  <span className="truncate">{enseigne.name}</span>
                </button>
              );
            })}
          </div>
        </div>
      </div>
    </div>
  );
}