import { getI18n } from '@/locales/server';
import SectionHeading from '../../ui/_sections/section-heading';

import StepOneAfflictionList from '../_components/step-one-affliction-list';
import StepTwoSufferingQuantification from '../_components/step-two-suffering-quantification';
import StepThreeSufferingSummary from '../_components/step-three-suffering-summary';
import SufferingScalesDescription from '@/app/[locale]/methodology/_components/suffering-scales-description';

export default async function SufferingQuantificationStepsSection() {
  const t = await getI18n();

  return (
    <section className="p-section bg-white">
      <div className="">
        <SectionHeading heading_number="1" title={t('MethodologyPage.sufferingQuantificationSteps.title')} />
        <div className="flex flex-col md:flex-row gap-6 py-8 uppercase">
          <StepOneAfflictionList />
          <StepTwoSufferingQuantification />
          <StepThreeSufferingSummary />
        </div>
        <SufferingScalesDescription display_criteria={true} />
      </div>
    </section>
  );
}
