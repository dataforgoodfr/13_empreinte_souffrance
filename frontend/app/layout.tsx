import type { Metadata } from 'next';
import './globals.css';
import { ReactElement } from 'react';
import { setStaticParamsLocale } from 'next-international/server';
import { Albert_Sans, Azeret_Mono } from 'next/font/google';

const azeretMono = Azeret_Mono({
  subsets: ['latin'],
  variable: '--font-azeret-mono',
});

const albertSans = Albert_Sans({
  subsets: ['latin'],
  variable: '--font-albert-sans',
});
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
      <body className={`antialiased bg-grey dark-text ${azeretMono.variable} ${albertSans.variable}`}>{children}</body>
    </html>
  );
}
