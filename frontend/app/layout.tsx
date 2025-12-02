import type { Metadata } from 'next';
import './globals.css';
import { ReactElement } from 'react';
import { setStaticParamsLocale } from 'next-international/server';
import { Albert_Sans } from 'next/font/google';


const albertSans = Albert_Sans({
  subsets: ['latin'],
  variable: '--font-albert-sans',
});

export const metadata: Metadata = {
  title: 'L’heure des comptes : pour la fin des poules en cages',
  description: 'Il y a 10 ans, les supermarchés s’engageaient à ne plus vendre aucun œuf de poule en cage d’ici fin 2025. Une nouvelle methode quanitife l’empreinte souffrance des poules pondeuses. Il est urgent de faire tenir les engamgements de la grande distribution et de mettre fin à l’élevage de poules pondeuses en cage',
robots: {
    index: true,
    follow: true,
  },
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
      <body className={`antialiased dark-text ${albertSans.variable}`}>{children}</body>
    </html>
  );
}
