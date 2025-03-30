import type { Metadata } from 'next';
import './globals.css';
import { ReactElement } from 'react';

export const metadata: Metadata = {
  title: 'Empreinte Souffrance',
  description: 'Site web empreinte souffrance',
};

export default async function RootLayout({
  params,
  children,
}: {
  params: Promise<{ locale: string }>;
  children: ReactElement;
}) {
  const { locale } = await params;

  return (
    <html lang={locale}>
      <body className="antialiased">{children}</body>
    </html>
  );
}
