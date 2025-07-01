import { getI18n } from '@/locales/server';
import SufferingQuantificationSteps from './suffering-quantification-steps';
import IntroductionSection from './introduction-section';
import MethodDetailsSection from './method-details-section';
import KeyResultsSection from './key-results-section';
import HeroBanner from '../ui/general/heroBanner';
import GoFurtherSection from '@/app/[locale]/ui/general/home-page/go-further-section';


export default async function MethodologyPage() {
  const t = await getI18n();

  return (
    <>
      <HeroBanner title={t('MethodologyPage.heroiBanner.title')} />
      <IntroductionSection />
      <SufferingQuantificationSteps />
      <MethodDetailsSection />
      <KeyResultsSection />
      <GoFurtherSection />
    </>
  );
}
