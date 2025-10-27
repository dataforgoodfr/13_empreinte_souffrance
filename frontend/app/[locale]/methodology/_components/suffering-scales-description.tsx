import { getI18n } from '@/locales/server';

interface SufferingScaleDescriptionProps {
  display_criteria?: boolean;
}

interface SufferingScale {
  title: string;
  stage_description: string;
  criteria_description: string;
  background_color: string;
  text_color?: string;
}

export default async function SufferingScalesDescription({ display_criteria = false }: SufferingScaleDescriptionProps) {
  const t = await getI18n();
  const suffering_stages: SufferingScale[] = [
    {
      title: t('PainEquationSection.stages.discomfort.title'),
      stage_description: t('PainEquationSection.stages.discomfort.text'),
      criteria_description: t('MethodologyPage.sufferingQuantificationSteps.legend.discomfort.criteria_description'),
      background_color: 'bg-pink-1',
    },
    {
      title: t('PainEquationSection.stages.pain.title'),
      stage_description: t('PainEquationSection.stages.pain.text'),
      criteria_description: t('MethodologyPage.sufferingQuantificationSteps.legend.pain.criteria_description'),
      background_color: 'bg-pink-2',
    },
    {
      title: t('PainEquationSection.stages.suffering.title'),
      stage_description: t('PainEquationSection.stages.suffering.text'),
      criteria_description: t('MethodologyPage.sufferingQuantificationSteps.legend.suffering.criteria_description'),
      background_color: 'bg-pink-3',
    },
    {
      title: t('PainEquationSection.stages.agony.title'),
      stage_description: t('PainEquationSection.stages.agony.text'),
      criteria_description: t('MethodologyPage.sufferingQuantificationSteps.legend.agony.criteria_description'),
      background_color: 'bg-brown',
      text_color: 'text-pink-1',
    },
  ];

  return (
    <>
      <h2 className="font-bold uppercase mt-6">{t('MethodologyPage.sufferingQuantificationSteps.title2')}</h2>
      <p className="md:max-w-2/3 my-6">{t('MethodologyPage.sufferingQuantificationSteps.text')}</p>
      <div className="grid grid-cols-1 md:grid-cols-4 gap-2">
        {suffering_stages.map((suffering_stage: SufferingScale, index) => (
          <article
            key={index}
            className={`flex flex-col gap-[20px] p-4 rounded-[16px] ${suffering_stage.background_color} ${suffering_stage.text_color}`}
          >
            <h4 className="font-bold uppercase mb-4 mt-4">{suffering_stage.title}</h4>
            <p className="text-body font-medium">{suffering_stage.stage_description}</p>

            {display_criteria && (
              <p className="pt-2 text-body">
                <span className="font-bold">{t('MethodologyPage.sufferingQuantificationSteps.criteria')} : </span>
                <span>{suffering_stage.criteria_description}</span>
              </p>
            )}
          </article>
        ))}
      </div>
    </>
  );
}
