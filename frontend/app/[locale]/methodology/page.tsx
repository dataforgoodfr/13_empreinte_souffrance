import SufferingQuantificationStepsSection from './_sections/three-steps-method-section';
import IntroductionSection from './_sections/introduction-section';
import MethodDetailsSection from './_sections/method-details-section';
import KeyResultsSection from './_sections/key-results-section';
import GoFurtherSection from '@/app/[locale]/ui/_sections/go-further-section';

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
