import { getI18n } from '@/locales/server';
import HeroSection from './hero-section';
import IntroductionSection from './introduction-section';
import MethodDetailsSection from './method-details-section';
import KeyResultsSection from './key-results-section';
import HeroBanner from '../ui/general/heroBanner';

export default async function MethodologyPage() {
  const t = await getI18n();

  return (
    <>
      <HeroBanner title={t('MethodologyPage.heroiBanner.title')} />
      <HeroSection />
      <IntroductionSection />
      <MethodDetailsSection />
      <KeyResultsSection />
    </>
  );
}
