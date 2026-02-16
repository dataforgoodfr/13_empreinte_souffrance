import Header from '@/app/[locale]/numbers/_components/Header';
import GoFurtherSection from '../ui/_sections/go-further-section';
import Section from '@/app/[locale]/numbers/_components/Section';

import StoreMapClient from '@/app/[locale]/numbers/_components/store-map-client';
import ProportionMarketVisited from '@/app/[locale]/numbers/_components/ProportionMarketVisited';
import ProportionCakeCagedEggs from './_components/ProportionCakeCagedEggs';
import EggsSalesFarmingMethod from './_components/EggsSalesFarmingMethod';
import ProportionCagedHen from './_components/ProportionCagedHen';
import MarketCommitmentDate from './_components/MarketCommitmentDate';

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

      {/* Carte des supermarchés */}
      <Section
        title={"PART D'OEUFS CAGE EN SUPERMARCHES"}
        text={
          '73 % des supermarchés vendent encore des œufs de poules en cage. C’est l’enseignement principal d’une enquête nationale menée par plus de 100 personnes dans 386 supermarchés en janvier.'
        }
        className="!px-1 md:!px-8 flex flex-col"
        innerClassName=""
        contentClassName="justify-end"
        anchorName={'carte'}
      >

        <StoreMapClient />
      </Section>

      <hr className="border border-pink-3 w-full max-w-[65%] mx-auto" />

      {/* Proportion des magasins ... */}
      <Section
        title={'Proportion des magasins visités où des œufs cage ont été trouvés (par enseigne)'}
        text={
          'Monoprix, ALDI et Intermarché se démarquent positivement, même si leur engagement n’est pas encore atteint. Dès septembre 2025, plus de 97 % des œufs vendus par Monoprix, ALDI et Intermarché étaient hors cage (chiffres communiqués par les enseignes). Des œufs de poules en cage ont été trouvés dans la grande majorité des magasins des 5 autres distributeurs, malgré leurs engagements.'
        }
      >
        <ProportionMarketVisited />
      </Section>

      <hr className="border border-pink-3 w-full max-w-[65%] mx-auto" />

      {/* Proportion des gateaux avec oeufs cages */}
      <Section
        title={'Proportion de brioches, gâteaux... de marque distributeur À base d’œufs 100% hors cage'}
        text={
          <>
            Sur les 25 références marque distributeur analysées chez toutes les enseignes, ce sont Lidl, Leclerc,
            Monoprix, ALDI et Lidl qui vendent le plus de références avec des œufs 100% hors cage (
            <a
              className="underline"
              target="_blank"
              href="https://drive.google.com/file/d/1Il1NsI1qQdP806HkiL7V87lOeMbPc9ZB/view"
            >
              exemple chez ALDI
            </a>
            ). Beaucoup d'œufs sont utilisés sous forme d'ingrédient dans les produits vendus en grande surface. Les
            supermarchés se sont engagés à ne plus utiliser d'œufs cage dans leurs marques distributeur à partir du 1er
            janvier 2026.
          </>
        }
      >
        <ProportionCakeCagedEggs />
      </Section>

      <hr className="border border-pink-3 w-full max-w-[65%] mx-auto" />

      {/* Vente d'oeufs selon mode d'élevage */}
      <Section
        title={'Ventes d’œufs en grande distribution en France, selon le mode d’élevage'}
        text={
          'Grâce aux engagements des supermarchés, la part d’œufs cage vendue en grande distribution est aujourd’hui historiquement basse, de 51 % en 2016 à 14 % en 2025. Cette évolution s’est faite au profit des œufs de poules élevées au sol et en plein air.'
        }
      >
        <EggsSalesFarmingMethod />
      </Section>

      <hr className="border border-pink-3 w-full max-w-[65%] mx-auto" />

      {/* Proportion poules en cage  */}
      <Section
        title={'Proportion de poules élevées en cage en France'}
        text={
          'Les engagements des entreprises ont eu un effet majeur sur les éleveurs de poules pondeuses qui ont mené une transition rapide vers des modes d’élevage hors cage (plein air et sol). Grâce à cela, ce sont chaque année 9 millions de poules qui peuvent connaître la lumière du jour et sentir la terre sous leurs pattes, plutôt que de subir une vie d’enfermement entre les barreaux d’une cage. Malheureusement, la transition vers la fin des cages freine depuis 2022. '
        }
      >
        <ProportionCagedHen />
      </Section>

      <hr className="border border-pink-3 w-full max-w-[65%] mx-auto" />

      {/* Date prise engagement  */}
      <Section
        title={'Dates de prise des engagements hors cage des supermarchés pour 2026'}
        text={
          <>
            La presse titrait il y a 10 ans sur les engagements hors cage de{' '}
            <a
              className="underline"
              target="_blank"
              href="https://www.lineaires.com/la-distribution/poules-en-cage-l-effet-domino#:~:text=En%20janvier%202017,ce%2010%20janvier"
            >
              Leclerc,{' '}
            </a>
            <a
              className="underline"
              target="_blank"
              href="https://www.huffingtonpost.fr/life/article/carrefour-va-arreter-de-vendre-des-ufs-de-poules-elevees-en-cage_90955.html"
            >
              Carrefour,{' '}
            </a>
            <a
              className="underline"
              target="_blank"
              href="https://www.quechoisir.org/actualite-oeufs-de-poules-en-cage-des-distributeurs-disent-stop-n23757/"
            >
              Intermarché,{' '}
            </a>
            <a
              className="underline"
              target="_blank"
              href="https://www.lsa-conso.fr/systeme-u-s-engage-a-ne-plus-vendre-d-oeufs-de-poule-elevees-en-cage-pour-sa-mdd-d-ici-a-2020,247602"
            >
              U,{' '}
            </a>
            <a
              className="underline"
              target="_blank"
              href="https://www.lefigaro.fr/flash-eco/2017/04/14/97002-20170414FILWWW00042-auchan-ne-vendra-plus-d-ufs-de-poules-en-cage.php"
            >
              Auchan,{' '}
            </a>
            <a
              className="underline"
              target="_blank"
              href="https://www.lafranceagricole.fr/2016/article/776953/lidl-france-annonce-larrt-des-ufs-de-poules-leves-en-cage"
            >
              Lidl,{' '}
            </a>
            <a
              className="underline"
              target="_blank"
              href="https://www.tf1info.fr/conso-argent/fini-les-oeufs-de-poules-en-batterie-chez-monoprix-cage-plein-air-bio-rappel-des-codes-1508102.html"
            >
              Monoprix,{' '}
            </a>
            <a
              className="underline"
              target="_blank"
              href="https://www.ouest-france.fr/europe/allemagne/son-tour-aldi-promet-den-finir-avec-les-oeufs-de-batterie-4402574"
            >
              et ALDI,{' '}
            </a>
            pour 2026.'
          </>
        }
      >
        <MarketCommitmentDate />
      </Section>

      <GoFurtherSection />
    </>
  );
}
