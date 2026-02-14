import GoFurtherSection from '../ui/_sections/go-further-section';
import Header from '@/app/[locale]/numbers/_components/Header';
import Supermarkets from '@/app/[locale]/numbers/_components/Supermarkets';
import Section from '@/app/[locale]/numbers/_components/Section';
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
        title={'Carte des magasins vendant encore des œufs cage'}
        text={
          '73 % des supermarchés vendent encore des œufs de poules en cage. C’est l’enseignement principal d’une enquête nationale menée par plus de 100 personnes dans 386 supermarchés en janvier.'
        }
        className="!px-1 md:!px-8"
        innerClassName=""
        contentClassName="justify-end"
        anchorName={'carte'}
      >
        <StoreMapClient />
      </Section>

      <hr className="border border-pink-3 w-full max-w-[250px] md:max-w-[620px] mx-auto" />

      <Section
        title="Proportion des magasins visités où des œufs cage ont été trouvés (par enseigne)"
        text={
          'Monoprix, ALDI et Intermarché se démarquent positivement, même si leur engagement n’est pas encore atteint. Dès septembre 2025, plus de 97 % des œufs vendus par Monoprix, ALDI et Intermarché étaient hors cage (chiffres communiqués par les enseignes). Des œufs de poules en cage ont été trouvés dans la grande majorité des magasins des 5 autres distributeurs, malgré leurs engagements.'
        }
      >
        <span>TODO graphe proporition magasin ici</span>
      </Section>

      <hr className="border border-pink-3 w-full max-w-[250px] md:max-w-[620px] mx-auto" />

      <Section
        title="Proportion de brioches, gâteaux... de marque distributeur À base d’œufs 100% hors cage"
        text={
          'Sur les 25 références marque distributeur analysées chez toutes les enseignes, ce sont Lidl, Leclerc, Monoprix, ALDI et Lidl qui vendent le plus de références avec des œufs 100% hors cage (exemple chez ALDI). Beaucoup d’œufs sont utilisés sous forme d’ingrédient dans les produits vendus en grande surface. Les supermarchés se sont engagés à ne plus utiliser d’œufs cage dans leurs marques distributeur à partir du 1er janvier 2026.'
        }
      >
        <span>TODO graphe marques distributeurs ici</span>
      </Section>

      <hr className="border border-pink-3 w-full max-w-[250px] md:max-w-[620px] mx-auto" />

      <Section
        title="Ventes d’œufs en grande distribution en France, selon le mode d’élevage"
        text={
          'Grâce aux engagements des supermarchés, la part d’œufs cage vendue en grande distribution est aujourd’hui historiquement basse, de 51 % en 2016 à 14 % en 2025. Cette évolution s’est faite au profit des œufs de poules élevées au sol et en plein air.'
        }
      >
        <span>TODO oeufs grande distrib ici</span>
      </Section>

      <hr className="border border-pink-3 w-full max-w-[250px] md:max-w-[620px] mx-auto" />

      <Section
        title="Proportion de poules élevées en cage en France"
        text={
          'Les engagements des entreprises ont eu un effet majeur sur les éleveurs de poules pondeuses qui ont mené une transition rapide vers des modes d’élevage hors cage (plein air et sol). Grâce à cela, ce sont chaque année 9 millions de poules qui peuvent connaître la lumière du jour et sentir la terre sous leurs pattes, plutôt que de subir une vie d’enfermement entre les barreaux d’une cage. Malheureusement, la transition vers la fin des cages freine depuis 2022.'
        }
      >
        <span>TODO poules élevées en cage ici</span>
      </Section>

      <hr className="border border-pink-3 w-full max-w-[250px] md:max-w-[620px] mx-auto" />

      <Section
        title="Dates de prise des engagements hors cage des supermarchés pour 2026"
        text={
          'La presse titrait il y a 10 ans sur les engagements hors cage de Leclerc, Carrefour, Intermarché, U, Auchan, Lidl, Monoprix et ALDI pour 2026.'
        }
      >
        <Supermarkets className="w-full h-full" />
      </Section>

      <GoFurtherSection />
    </>
  );
}
