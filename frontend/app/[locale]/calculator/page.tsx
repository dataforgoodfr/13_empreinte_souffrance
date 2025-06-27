import { getI18n } from '@/locales/server';
import CalculatorHeroSection from './calculator-hero-section';
import MethodDetailsSection from './method-details-section';
import SelectorSection from './calculator-selector-section';
import HeroBanner from '../ui/general/heroBanner';

export default async function Calculator() {
  const t = await getI18n();

  return (
    <>
      <HeroBanner title={t('calculatorPage.heroBanner.title')} />
      <CalculatorHeroSection />
      <SelectorSection />
      <MethodDetailsSection />
    </>
  );
}
