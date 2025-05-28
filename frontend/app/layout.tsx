import type { Metadata } from 'next';
import './globals.css';
import { ReactElement } from 'react';
import { setStaticParamsLocale } from 'next-international/server';

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
  setStaticParamsLocale(locale);

  return (
    <html lang={locale}>
      <body className="antialiased bg-red-50">{children}</body>
    </html>
  );
}
