import type { Metadata } from 'next';
import 'leaflet/dist/leaflet.css';

export const metadata: Metadata = {
  title: 'Store Map Embed',
};

export default function EmbedLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return <>{children}</>;
}
