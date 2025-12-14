import GoFurtherSection from '../ui/_sections/go-further-section';
import Header from '@/app/[locale]/numbers/_components/Header';
import Supermarkets from '@/app/[locale]/numbers/_components/Supermarkets';
import Section from '@/app/[locale]/numbers/_components/Section';
import CagedEggsGraph from '@/app/[locale]/numbers/_components/CagedEggs';
import StoreMap from '@/app/[locale]/numbers/_components/store-map';

export default async function NumbersPage() {
  return (
    <section className="flex flex-col items-center gap-8">
      <Header />
      <Section
        title="DATES DES ENGAGEMENTS HORS CAGE DES SUPERMARCHES"
        text={
          'Il y a 10 ans, les supermarchés s’engageaient à ne plus vendre aucun œuf de poule en cage d’ici fin 2025. Ces engagements concernent aussi bien les oeufs frais, que les oeufs utilisés dans les produits à marque distributeur (pâtes fraîches aux oeufs, brioche, gâteaux…etc).'
        }
      >
        <Supermarkets className="w-full h-full" />
      </Section>
      <Section
        title={'SUPERMARCHES VENDANT ENCORE DES ŒUFS CAGE'}
        text={
          'Une grande enquête menée en janvier 2026 a montré que xxx supermachés continuaient de vendre des œufs cage. Pourtant, plus aucun oeuf cage ne devrait se trouver en supermarché selon les engagements.'
        }
        className={'h-[70vh]'}
      >
        <CagedEggsGraph />
      </Section>
      <Section
        title={'PART D’OEUFS CAGE EN SUPERMARCHES'}
        text={
          'La cage occupait encore une part minoriaire mais signifcative en 2025. Le plein air est le mode délevage le plus répandu en supermarché. '
        }
      >
        <StoreMap />
      </Section>
      <GoFurtherSection />
    </section>
  );
}
