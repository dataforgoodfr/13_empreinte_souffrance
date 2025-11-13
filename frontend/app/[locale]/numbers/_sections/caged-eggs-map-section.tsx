'use client';

import { MapContainer, TileLayer, CircleMarker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';

type Store = {
  name: string;
  coords: [number, number];
  category: string;
  address: string;
  color: string;
  status: string;
};

const stores: Store[] = [
  // Carrefour
  {
    name: 'Carrefour Paris',
    coords: [48.8566, 2.3522],
    category: 'carrefour',
    address: '85 Quai de Bercy, 75012 Paris',
    color: '',
    status: '',
  },
  {
    name: 'Carrefour Lyon',
    coords: [45.764, 4.8357],
    category: 'carrefour',
    address: '17 Rue du Docteur Bouchut, 69003 Lyon',
    color: '',
    status: '',
  },
  {
    name: 'Carrefour Marseille',
    coords: [43.2965, 5.3698],
    category: 'carrefour',
    address: 'Avenue de Hambourg, 13008 Marseille',
    color: '',
    status: '',
  },
  // Auchan
  {
    name: 'Auchan Lille',
    coords: [50.6292, 3.0573],
    category: 'auchan',
    address: '135 Boulevard de la Liberté, 59000 Lille',
    color: '',
    status: '',
  },
  {
    name: 'Auchan Toulouse',
    coords: [43.6045, 1.444],
    category: 'auchan',
    address: '2 Avenue de Fronton, 31200 Toulouse',
    color: '',
    status: '',
  },
  {
    name: 'Auchan Bordeaux',
    coords: [44.8378, -0.5792],
    category: 'auchan',
    address: 'Rue Achard, 33300 Bordeaux',
    color: '',
    status: '',
  },
  // Lidl
  {
    name: 'Lidl Nantes',
    coords: [47.2184, -1.5536],
    category: 'lidl',
    address: '12 Boulevard de Berlin, 44000 Nantes',
    color: '',
    status: '',
  },
  {
    name: 'Lidl Strasbourg',
    coords: [48.5734, 7.7521],
    category: 'lidl',
    address: '45 Route du Rhin, 67100 Strasbourg',
    color: '',
    status: '',
  },
  {
    name: 'Lidl Nice',
    coords: [43.7102, 7.262],
    category: 'lidl',
    address: '28 Avenue Malausséna, 06000 Nice',
    color: '',
    status: '',
  },
  // Leclerc
  {
    name: 'Leclerc Rennes',
    coords: [48.1173, -1.6778],
    category: 'leclerc',
    address: 'Rue de la Rigourdière, 35510 Cesson-Sévigné',
    color: '',
    status: '',
  },
  {
    name: 'Leclerc Montpellier',
    coords: [43.6108, 3.8767],
    category: 'leclerc',
    address: 'Avenue de Palavas, 34000 Montpellier',
    color: '',
    status: '',
  },
  {
    name: 'Leclerc Dijon',
    coords: [47.322, 5.0415],
    category: 'leclerc',
    address: 'Boulevard Eugène Fyot, 21000 Dijon',
    color: '',
    status: '',
  },
  // Super U
  {
    name: 'Super U Angers',
    coords: [47.4784, -0.5632],
    category: 'superu',
    address: '15 Rue des Lices, 49100 Angers',
    color: '',
    status: '',
  },
  {
    name: 'Super U Rouen',
    coords: [49.4431, 1.0993],
    category: 'superu',
    address: "32 Rue Jeanne d'Arc, 76000 Rouen",
    color: '',
    status: '',
  },
  {
    name: 'Super U Avignon',
    coords: [43.9493, 4.8055],
    category: 'superu',
    address: 'Avenue Pierre Sémard, 84000 Avignon',
    color: '',
    status: '',
  },
];

// assign colors & statuses randomly like the vanilla JS version
stores.forEach((store) => {
  store.color = Math.random() < 0.5 ? 'red' : 'green';
  store.status = store.color === 'red' ? "Présence d'œufs cage" : "Pas d'œufs cage";
});

export default function SimpleStoreMap() {
  return (
    <div style={{ height: '100vh', width: '100%' }}>
      <MapContainer
        center={[46.5, 2.5]}
        zoom={6}
        scrollWheelZoom
        style={{ height: '100%', width: '100%' }}
        minZoom={5}
        maxZoom={10}
      >
        <TileLayer
          url="https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png"
          attribution='&copy; <a href="https://www.carto.com/">CARTO</a>'
          subdomains="abcd"
        />

        {stores.map((store, i) => (
          <CircleMarker
            key={i}
            center={store.coords}
            radius={8}
            pathOptions={{
              fillColor: store.color,
              fillOpacity: 0.9,
              color: 'white',
              weight: 2,
            }}
          >
            <Popup>
              <div>
                <b>{store.name}</b>
                <br />
                {store.address}
                <br />
                <i>{store.category}</i>
                <br />
                <span>{store.status}</span>
              </div>
            </Popup>
          </CircleMarker>
        ))}
      </MapContainer>
    </div>
  );
}
