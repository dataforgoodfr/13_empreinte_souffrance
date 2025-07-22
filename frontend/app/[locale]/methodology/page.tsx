import SufferingQuantificationStepsSection from './_section/suffering-quantification-steps-section';
import IntroductionSection from './_section/introduction-section';
import MethodDetailsSection from './_section/method-details-section';
import KeyResultsSection from './_section/key-results-section';

import GoFurtherSection from '@/app/[locale]/ui/_section/go-further-section';

export default async function MethodologyPage() {
  return (
    <>
      <IntroductionSection />
      <SufferingQuantificationStepsSection />
      <MethodDetailsSection />
      <KeyResultsSection />
      <GoFurtherSection />
    </>
  );
}
