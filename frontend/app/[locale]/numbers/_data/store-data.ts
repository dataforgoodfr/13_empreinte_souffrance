type Store = {
  name: string;
  coords: [number, number];
  category: string;
  address: string;
  hasCageEggs: boolean; // true = présence d'œufs cage, false = pas d'œufs cage
};

export const store: Store[] = [

  {
    name: 'Carrefour Paris',
    coords: [48.8566, 2.3522],
    category: 'carrefour',
    address: '85 Quai de Bercy, 75012 Paris',
    hasCageEggs: true,
  },
  {
    name: 'Carrefour Lyon',
    coords: [45.764, 4.8357],
    category: 'carrefour',
    address: '17 Rue du Docteur Bouchut, 69003 Lyon',
    hasCageEggs: false,
  },
  {
    name: 'Carrefour Marseille',
    coords: [43.2965, 5.3698],
    category: 'carrefour',
    address: 'Avenue de Hambourg, 13008 Marseille',
    hasCageEggs: true,
  },
  
  {
    name: 'Auchan Lille',
    coords: [50.6292, 3.0573],
    category: 'auchan',
    address: '135 Boulevard de la Liberté, 59000 Lille',
    hasCageEggs: true,
  },
  {
    name: 'Auchan Toulouse',
    coords: [43.6045, 1.444],
    category: 'auchan',
    address: '2 Avenue de Fronton, 31200 Toulouse',
    hasCageEggs: false,
  },
  {
    name: 'Auchan Bordeaux',
    coords: [44.8378, -0.5792],
    category: 'auchan',
    address: 'Rue Achard, 33300 Bordeaux',
    hasCageEggs: true,
  },
  
  {
    name: 'Lidl Nantes',
    coords: [47.2184, -1.5536],
    category: 'lidl',
    address: '12 Boulevard de Berlin, 44000 Nantes',
    hasCageEggs: false,
  },
  {
    name: 'Lidl Strasbourg',
    coords: [48.5734, 7.7521],
    category: 'lidl',
    address: '45 Route du Rhin, 67100 Strasbourg',
    hasCageEggs: false,
  },
  {
    name: 'Lidl Nice',
    coords: [43.7102, 7.262],
    category: 'lidl',
    address: '28 Avenue Malaussena, 06000 Nice',
    hasCageEggs: true,
  },
  
  {
    name: 'Leclerc Rennes',
    coords: [48.1173, -1.6778],
    category: 'leclerc',
    address: 'Rue de la Rigoudière, 35510 Cesson-Sévigné',
    hasCageEggs: false,
  },
  {
    name: 'Leclerc Montpellier',
    coords: [43.6108, 3.8767],
    category: 'leclerc',
    address: 'Avenue de Palavas, 34000 Montpellier',
    hasCageEggs: true,
  },
  {
    name: 'Leclerc Dijon',
    coords: [47.322, 5.0415],
    category: 'leclerc',
    address: 'Boulevard Eugène Fyot, 21000 Dijon',
    hasCageEggs: false,
  },
  
  {
    name: 'Super U',
    coords: [47.4784, -0.5632],
    category: 'superu',
    address: '15 Rue des Lices, 49100 Angers',
    hasCageEggs: true,
  },
  {
    name: 'Super U',
    coords: [49.4431, 1.0993],
    category: 'superu',
    address: "32 Rue Jeanne d'Arc, 76000 Rouen",
    hasCageEggs: true,
  },
  {
    name: 'Super U Avignon',
    coords: [43.9493, 4.8055],
    category: 'superu',
    address: 'Avenue Pierre Sémard, 84000 Avignon',
    hasCageEggs: false,
  },
];


export type EnseigneConfig = {
  id: string;
  name: string;
  logo: string; 
};

export const enseignes: EnseigneConfig[] = [
  {
    id: 'carrefour',
    name: 'Carrefour',
    logo: '/logo/carrefour_logo.svg', 
  },
  {
    id: 'auchan',
    name: 'Auchan',
    logo: '/logo/auchan_logo.svg',
  },
  {
    id: 'lidl',
    name: 'Lidl',
    logo: '/logo/lidl_logo.svg', 
  },
  {
    id: 'leclerc',
    name: 'Leclerc',
    logo: '/logo/leclerc_logo.png', 
  },
  {
    id: 'superu',
    name: 'Super U',
    logo: '/logo/U_logo.png',
  },
    {
    id: 'aldi',
    name: 'Aldi',
    logo: '/logo/aldi_logo.svg',
  },
      {
    id: 'monoprix',
    name: 'Monoprix',
    logo: '/logo/monoprix_logo.svg',
  },
      {
    id: 'casino',
    name: 'Casino',
    logo: '/logo/casino_logo.svg',
  },
      {
    id: 'intermarche',
    name: 'Intermarché',
    logo: '/logo/intermarche_logo.png',
  },

];