
import ResultsSection from '@/app/[locale]/home/_sections/results-section';
import GoFurtherSection from '@/app/[locale]/ui/_sections/go-further-section';
import ProgressSection from './home/_sections/progress-section';
import HeroPressSection from './home/_sections/hero-press-section';
import PromiseKeptSection from './home/_sections/promise-kept-section';

import { Metadata } from 'next';
export const metadata: Metadata = {
  title: 'Accueil',
  description: "L’heure des comptes révèle si les supermarchés ont tenu leur promesse de ne plus vendre d’œufs de poules en cage, en s’appuyant sur une enquête d’Anima.",
  keywords: [
    'engagement supermarchés œufs cage',
    'promesse 2026',
    'œufs cage France',
    'enquête Anima 2026',
    'bannir œufs cages',
    'supermarchés œufs éthiques',
    'heure des comptes',
    'promesse tenue supermarchés',
  ],
  openGraph: {
    title: 'Promesse tenue ? C\'est l\'heure des comptes - Anima',
    description: "L’heure des comptes révèle si les supermarchés ont tenu leur promesse de ne plus vendre d’œufs de poules en cage, en s’appuyant sur une enquête d’Anima.",
    images: ['/og-image.png'],
  },
  twitter: {
    title: 'Promesse tenue ? C\'est l\'heure des comptes - Anima',
   description: "L’heure des comptes révèle si les supermarchés ont tenu leur promesse de ne plus vendre d’œufs de poules en cage, en s’appuyant sur une enquête d’Anima.",
    images: ['/og-image.png'],
  },
  alternates: {
    canonical: '/',
  },
};

export default function Home() {
  return (
    <>
      <HeroPressSection />
      <PromiseKeptSection />
      <ProgressSection />
      <ResultsSection />
      <GoFurtherSection />
    </>
  );
}
