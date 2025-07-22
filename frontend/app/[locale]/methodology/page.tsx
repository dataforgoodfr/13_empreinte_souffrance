import SufferingQuantificationSteps from './suffering-quantification-steps';
import IntroductionSection from './introduction-section';
import MethodDetailsSection from './method-details-section';
import KeyResultsSection from './key-results-section';
import GoFurtherSection from '@/app/[locale]/ui/general/home-page/go-further-section';
import PainTrackTable from '../ui/general/pain_track_suffering';


export default async function MethodologyPage() {


  return (
    <>
      <IntroductionSection />
      <SufferingQuantificationSteps />
      <MethodDetailsSection />
      <PainTrackTable/>
      <KeyResultsSection />
      <GoFurtherSection />
    </>
  );
}
