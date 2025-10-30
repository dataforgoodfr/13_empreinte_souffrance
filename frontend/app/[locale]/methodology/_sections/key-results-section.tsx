import SectionHeading from '../../ui/_sections/section-heading';
import { getI18n } from '@/locales/server';
import SufferingScales from '@/app/[locale]/methodology/_components/suffering-scales';

export default async function KeyResultsSection() {
  const t = await getI18n();

  return (
    <section className="bg-pink-2 p-section">
      <div className="">
        <SectionHeading title={t('MethodologyPage.key_results_section.key_results_h1')} heading_number="3" />
        <div className="text-lead">
          <p>{t('MethodologyPage.key_results_section.quantify_suffering_description')}</p>
          <p className="py-4">{t('MethodologyPage.key_results_section.calculation_method_description')}</p>
        </div>
        <div className="grid md:grid-cols-2 grid-cols-1 gap-2 ">
          <AfflictionResultCard
            text={t('MethodologyPage.key_results_section.caged_hen_card.title')}
            agony={t('MethodologyPage.key_results_section.caged_hen_card.agony')}
            pain={t('MethodologyPage.key_results_section.caged_hen_card.pain')}
            suffering={t('MethodologyPage.key_results_section.caged_hen_card.suffering')}
            discomfort={t('MethodologyPage.key_results_section.caged_hen_card.discomfort')}
          />
          <AfflictionResultCard
            text={t('MethodologyPage.key_results_section.barn_raised_hen_card.title')}
            agony={t('MethodologyPage.key_results_section.barn_raised_hen_card.agony')}
            pain={t('MethodologyPage.key_results_section.barn_raised_hen_card.pain')}
            suffering={t('MethodologyPage.key_results_section.barn_raised_hen_card.suffering')}
            discomfort={t('MethodologyPage.key_results_section.barn_raised_hen_card.discomfort')}
          />
          <AfflictionResultCard
            text={t('MethodologyPage.key_results_section.caged_hen_egg_card.title')}
            agony={t('MethodologyPage.key_results_section.caged_hen_egg_card.agony')}
            pain={t('MethodologyPage.key_results_section.caged_hen_egg_card.pain')}
            suffering={t('MethodologyPage.key_results_section.caged_hen_egg_card.suffering')}
            discomfort={t('MethodologyPage.key_results_section.caged_hen_egg_card.discomfort')}
          />
          <AfflictionResultCard
            text={t('MethodologyPage.key_results_section.barn_raised_hen_egg_card.title')}
            agony={t('MethodologyPage.key_results_section.barn_raised_hen_egg_card.agony')}
            pain={t('MethodologyPage.key_results_section.barn_raised_hen_egg_card.pain')}
            suffering={t('MethodologyPage.key_results_section.barn_raised_hen_egg_card.suffering')}
            discomfort={t('MethodologyPage.key_results_section.barn_raised_hen_egg_card.discomfort')}
          />
        </div>
      </div>
    </section>
  );
}

//* Sub-components ________________________


interface AfflictionResultCardProps {
  text: string;
  agony: string;
  pain: string;
  suffering: string;
  discomfort: string;
}

const AfflictionResultCard = ({ text, agony, pain, suffering, discomfort }: AfflictionResultCardProps) => {
  return (
    <div className=" flex items-center bg-grey p-section gap-2 rounded-[10px]">
   
        <p className='uppercase font-bold text-h4 w-1/2'>{text}</p>
  
      <div className="flex flex-col items-center justify-center gap-2 w-1/2">
        <SufferingScales
          agony_duration_text={agony}
          pain_duration_text={pain}
          suffering_duration_text={suffering}
          discomfort_duration_text={discomfort}
        />
      </div>
    </div>
  );
};
