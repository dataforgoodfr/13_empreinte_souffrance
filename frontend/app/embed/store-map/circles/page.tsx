import StoreMapClient from '@/app/[locale]/numbers/_components/store-map-client';

/**
  Embeddable Store Map — circle markers variant.
 
  Usage:
 
    <iframe
      src="https://lheuredescomptes.org/embed/store-map/circles"
      width="500"
      height="700"
    ></iframe>
 */
export default function EmbedStoreMapCirclesPage() {
  return (
    <main className="w-screen h-screen">
      <StoreMapClient initialStyle="circle" initialSize={27} />
    </main>
  );
}
