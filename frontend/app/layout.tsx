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
    default: 'L’heure des comptes',
    template: '%s | L’heure des comptes',
  },
  description:
    'Il y a 10 ans, les supermarchés s’engageaient à ne plus vendre aucun œuf de poule en cage d’ici fin 2025. Ont-ils tenus leurs engagements ? C’est l’heure des comptes',
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
    title: 'L’heure des comptes',
    description:
      'Il y a 10 ans, les supermarchés s’engageaient à ne plus vendre aucun œuf de poule en cage d’ici fin 2025. Ont-ils tenus leurs engagements ? C’est l’heure des comptes',
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
    title: 'L’heure des comptes',
    description:
      'Il y a 10 ans, les supermarchés s’engageaient à ne plus vendre aucun œuf de poule en cage d’ici fin 2025. Ont-ils tenus leurs engagements ? C’est l’heure des comptes',
    images: ['/og-image.png'],
  },
  icons: {
    icon: '/favicon/favicon.ico',
    shortcut: '/favicon/favicon.ico',
  },
};

export default function RootLayout({ params, children }: { params: { locale: string }; children: ReactElement }) {
  const { locale } = params;
  setStaticParamsLocale(locale);

  return (
    <html lang={locale}>
      <body className={`antialiased dark-text ${albertSans.variable}`}>{children}</body>
    </html>
  );
}
