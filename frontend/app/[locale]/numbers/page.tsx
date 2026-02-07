import GoFurtherSection from '../ui/_sections/go-further-section';
import Header from '@/app/[locale]/numbers/_components/Header';
import Supermarkets from '@/app/[locale]/numbers/_components/Supermarkets';
import Section from '@/app/[locale]/numbers/_components/Section';
import CagedEggsGraph from '@/app/[locale]/numbers/_components/CagedEggs';
import StoreMapClient from '@/app/[locale]/numbers/_components/store-map-client';
import { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Les chiffres',
  description:
    "Découvrez les chiffres clés de l'enquête sur les œufs de poules en cage : engagements des supermarchés, résultats de terrain et statistiques détaillées.",
  keywords: ['statistiques œufs cage', 'chiffres supermarchés', 'enquête terrain', 'données bien-être animal'],
  openGraph: {
    title: "Les chiffres - L'heure des comptes",
    description:
      "Découvrez les chiffres clés de l'enquête sur les œufs de poules en cage : engagements des supermarchés, résultats de terrain et statistiques détaillées.",
    images: ['/og-numbers.png'],
  },
  twitter: {
    title: "Les chiffres - L'heure des comptes",
    description:
      "Découvrez les chiffres clés de l'enquête sur les œufs de poules en cage : engagements des supermarchés, résultats de terrain et statistiques détaillées.",
    images: ['/og-numbers.png'],
  },
  alternates: {
    canonical: '/numbers',
  },
};

export default async function NumbersPage() {
  return (
    <>
      <Header />

      <Section
        title="DATES DES ENGAGEMENTS HORS CAGE DES SUPERMARCHES"
        text={
          'Il y a 10 ans, les supermarchés s’engageaient à ne plus vendre aucun œuf de poule en cage d’ici fin 2025. Ces engagements concernent aussi bien les oeufs frais, que les oeufs utilisés dans les produits à marque distributeur (pâtes fraîches aux oeufs, brioche, gâteaux…etc).'
        }
      >
        <Supermarkets className="w-full h-full" />
      </Section>

      <hr className="flex justify-self-center border border-pink-3 w-full max-w-[250px] md:max-w-[620px]" />

      <Section
        title={'SUPERMARCHES VENDANT ENCORE DES ŒUFS CAGE'}
        text={
          'Une grande enquête menée en janvier 2026 a montré que xxx supermachés continuaient de vendre des œufs cage. Pourtant, plus aucun oeuf cage ne devrait se trouver en supermarché selon les engagements.'
        }
      >
        <CagedEggsGraph />
      </Section>

      <hr className="border justify-self-center border-pink-3 w-full max-w-[250px] md:max-w-[620px]" />

      <Section
        title={'PART D’OEUFS CAGE EN SUPERMARCHES'}
        text={
          'La cage occupait encore une part minoriaire mais signifcative en 2025. Le plein air est le mode délevage le plus répandu en supermarché. '
        }
      >
        <StoreMapClient />
      </Section>

      <GoFurtherSection />
    </>
  );
}
