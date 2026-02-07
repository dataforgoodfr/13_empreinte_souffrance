import StoreMapClient from '@/app/[locale]/numbers/_components/store-map-client';

/**
 * Embeddable Store Map page.
 *
 * Usage:
 *
 *   <iframe
 *     src="https://lheuredescomptes.org/embed/store-map"
 *     width="500"
 *     height="700"
 *   ></iframe>
 *
 * ───────────────────────────────────────────────────────────────────────────
 */
export default function EmbedStoreMapPage() {
  return (
    <main className="w-screen h-screen">
      <StoreMapClient />
    </main>
  );
}
