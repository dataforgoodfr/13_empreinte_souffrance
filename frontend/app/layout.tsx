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
  metadataBase: new URL('https://lheuredescomptes.org'),
  title: {
    default: 'L’heure des comptes - Anima x Data For Good',
    template: '%s | L’heure des comptes - Anima x Data For Good',
  },
  description:
    'L’heure des comptes révèle si les supermarchés ont tenu leur promesse de ne plus vendre d’œufs de poules en cage, en s’appuyant sur une enquête d’Anima.',
  robots: {
    index: true,
    follow: true,
  },

  alternates: {
    canonical: '/',
    languages: {
      fr: '/',
      en: '/en',
    },
  },

  openGraph: {
    title: 'L’heure des comptes - Anima x Data For Good',
    description:
      'L’heure des comptes révèle si les supermarchés ont tenu leur promesse de ne plus vendre d’œufs de poules en cage, en s’appuyant sur une enquête d’Anima.',
    url: 'https://lheuredescomptes.org',
    siteName: 'L’heure des comptes',
    locale: 'fr',
    type: 'website',
    images: [
      {
        url: '/og-image.png',
        width: 1200,
        height: 630,
        alt: "page d'accueil du site",
      },
    ],
  },
  twitter: {
    card: 'summary_large_image',
    title: 'L’heure des comptes - Anima x Data For Good',
    description:
      'L’heure des comptes révèle si les supermarchés ont tenu leur promesse de ne plus vendre d’œufs de poules en cage, en s’appuyant sur une enquête d’Anima.',
    images: ['/og-image.png'],
  },
  icons: {
    icon: '/favicon/favicon.ico',
    shortcut: '/favicon/favicon.ico',
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
      <body className={`antialiased text-black ${albertSans.variable}`}>{children}</body>
    </html>
  );
}
