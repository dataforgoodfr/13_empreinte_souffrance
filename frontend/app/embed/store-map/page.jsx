'use client';

import dynamic from 'next/dynamic';

// Import dynamique pour éviter les erreurs SSR avec Leaflet
const StoreMap = dynamic(
  () => import('@/app/[locale]/numbers/_components/store-map'),
  { ssr: false }
);

export default function EmbedStoreMapPage() {
  return (
    <div style={{ 
      width: '100%', 
      height: '100vh',
      margin: 0,
      padding: 0,
      overflow: 'hidden'
    }}>
      <StoreMap />
    </div>
  );
}