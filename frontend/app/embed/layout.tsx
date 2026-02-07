import type { Metadata } from 'next';
import { ReactNode } from 'react';

export const metadata: Metadata = {
  title: "Carte des supermarchés - L'heure des comptes",
  description:
    "Carte interactive des supermarchés vendant des œufs de poules en cage en France.",
  robots: {
    index: false,
    follow: false,
  },
};

/**
 * Minimal layout for embeddables
 */
export default function EmbedLayout({ children }: { children: ReactNode }) {
  return <div className="m-0 p-0 overflow-hidden">{children}</div>;
}
