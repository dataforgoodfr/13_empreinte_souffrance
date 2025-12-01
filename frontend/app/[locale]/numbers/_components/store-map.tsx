'use client';

import dynamic from 'next/dynamic';
import { store } from '../_data/store-data';

// On charge Plotly uniquement côté client
const Plot = dynamic(() => import('react-plotly.js'), {
  ssr: false,
});

export default function StoreMap() {
  // On enrichit les points avec status + color
  const enriched = store.map((s) => {
    const hasCageEggs = Math.random() < 0.5;
    const status = hasCageEggs
      ? "Présence d'œufs cage"
      : "Pas d'œufs cage";
    const color = hasCageEggs ? 'red' : 'green';
    return { ...s, status, color };
  });

  // Deux groupes pour une légende propre
  const withCage = enriched.filter((s) => s.status === "Présence d'œufs cage");
  const withoutCage = enriched.filter((s) => s.status === "Pas d'œufs cage");

  // Helper pour construire une trace Plotly
  const makeTrace = (points, name, color) => ({
    type: 'scattergeo',
    mode: 'markers',
    name,               // label dans la légende
    lat: points.map((p) => p.coords[0]),
    lon: points.map((p) => p.coords[1]),
    marker: {
      size: 12,
      color,
      line: { width: 1, color: 'white' },
      opacity: 0.9,
    },
    text: points.map(
      (p) =>
        `<b>${p.name}</b><br>${p.address}<br>${p.category}<br>${p.status}`
    ),
    hoverinfo: 'text',     // “popup” au survol
    showlegend: true,
  });

  const data = [
    makeTrace(withCage, "Présence d'œufs cage", 'red'),
    makeTrace(withoutCage, "Pas d'œufs cage", 'green'),
  ];

  return (
    <div style={{ width: '100%', height: '70vh' }}>
      <Plot
        data={data}
        layout={{
          geo: {
            // On cadre sur la France / Europe occidentale
            scope: 'europe',
            center: { lat: 46.5, lon: 2.5 },
            lonaxis: { range: [-5.5, 9.8] },
            lataxis: { range: [41, 51.5] },
            projection: { type: 'mercator' },

            // Fond de carte vectoriel gratuit (Pas de token)
            showland: true,
            landcolor: '#f0f0f0',
            showcountries: true,
            countrycolor: '#b0b0b0',
            showocean: true,
            oceancolor: '#dbeeff',
            showlakes: true,
            lakecolor: '#dbeeff',
            bgcolor: 'white',
          },
          legend: {
            x: 0.02,
            y: 0.98,
            bgcolor: 'rgba(255,255,255,0.9)',
            bordercolor: '#ccc',
            borderwidth: 1,
          },
          margin: { t: 0, b: 0, l: 0, r: 0 },
        }}
        config={{
          responsive: true,
          displayModeBar: false, // tu peux mettre true si tu veux les outils
        }}
        useResizeHandler={true}
        style={{ width: '100%', height: '100%' }}
      />
    </div>
  );
}
