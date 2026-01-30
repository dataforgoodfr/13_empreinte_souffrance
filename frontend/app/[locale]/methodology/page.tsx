import ThreeStepsMethodSection from './_sections/three-steps-method-section';
import IntroductionSection from './_sections/introduction-section';
import MethodDetailsSection from './_sections/method-details-section';
import KeyResultsSection from './_sections/key-results-section';
import GoFurtherSection from '@/app/[locale]/ui/_sections/go-further-section';
import { Metadata } from 'next';

export const metadata: Metadata = {
  title: "La vie d'une poule",
  description: "Découvrez la méthodologie qui qualifie scientifiquement la vie d'une poule en cage",
  keywords: ['méthodologie enquête', 'vie poule pondeuse', 'souffrance animale', 'bien-être poules', 'élevage cage'],
  openGraph: {
    title: "La vie d'une poule - L'heure des comptes",
    description: "Découvrez la méthodologie qui qualifie scientifiquement la vie d'une poule en cage",
    images: ['/og-methodology.png'],
  },
  twitter: {
    title: "La vie d'une poule - L'heure des comptes",
    description: "Découvrez la méthodologie qui qualifie scientifiquement la vie d'une poule en cage",
    images: ['/og-methodology.png'],
  },
  alternates: {
    canonical: '/methodology',
  },
};

export default async function MethodologyPage() {
  return (
    <>
      <IntroductionSection />
      <ThreeStepsMethodSection />
      <MethodDetailsSection />
      <KeyResultsSection />
      <GoFurtherSection />
    </>
  );
}
