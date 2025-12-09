import { getI18n } from '@/locales/server';
import { AnimatedAfflictionsGroup } from './animated-afflictions';
import SufferingScales from '@/app/[locale]/methodology/_components/suffering-scales';

export default async function ComputePainSources() {
  const t = await getI18n();

  const afflictions = [
    {
      title: t('MethodologyPage.sufferingQuantificationSteps.step3.bloc1.title'),
      percent: '40%',
      text: t('MethodologyPage.sufferingQuantificationSteps.step3.text1'),
      agony: t('MethodologyPage.sufferingQuantificationSteps.step3.bloc1.agony'),
      pain: t('MethodologyPage.sufferingQuantificationSteps.step3.bloc1.pain'),
      suffering: t('MethodologyPage.sufferingQuantificationSteps.step3.bloc1.suffering'),
      discomfort: t('MethodologyPage.sufferingQuantificationSteps.step3.bloc1.discomfort'),
    },
    {
      title: t('MethodologyPage.sufferingQuantificationSteps.step3.bloc2.title'),
      percent: '100%',
      text: t('MethodologyPage.sufferingQuantificationSteps.step3.text1'),
      agony: t('MethodologyPage.sufferingQuantificationSteps.step3.bloc2.agony'),
      pain: t('MethodologyPage.sufferingQuantificationSteps.step3.bloc2.pain'),
      suffering: t('MethodologyPage.sufferingQuantificationSteps.step3.bloc2.suffering'),
      discomfort: t('MethodologyPage.sufferingQuantificationSteps.step3.bloc2.discomfort'),
    },
    {
      title: t('MethodologyPage.sufferingQuantificationSteps.step3.bloc3.title'),
      percent: '48%',
      text: t('MethodologyPage.sufferingQuantificationSteps.step3.text1'),
      agony: t('MethodologyPage.sufferingQuantificationSteps.step3.bloc3.agony'),
      pain: t('MethodologyPage.sufferingQuantificationSteps.step3.bloc3.pain'),
      suffering: t('MethodologyPage.sufferingQuantificationSteps.step3.bloc3.suffering'),
      discomfort: t('MethodologyPage.sufferingQuantificationSteps.step3.bloc3.discomfort'),
    },
    {
      title: t('MethodologyPage.sufferingQuantificationSteps.step3.bloc4.title'),
      percent: '100%',
      text: t('MethodologyPage.sufferingQuantificationSteps.step3.text1'),
      agony: t('MethodologyPage.sufferingQuantificationSteps.step3.bloc4.agony'),
      pain: t('MethodologyPage.sufferingQuantificationSteps.step3.bloc4.pain'),
      suffering: t('MethodologyPage.sufferingQuantificationSteps.step3.bloc4.suffering'),
      discomfort: t('MethodologyPage.sufferingQuantificationSteps.step3.bloc4.discomfort'),
    },
    {
      title: t('MethodologyPage.sufferingQuantificationSteps.step3.bloc6.title'),
      percent: '0,525%',
      text: t('MethodologyPage.sufferingQuantificationSteps.step3.text1'),
      agony: t('MethodologyPage.sufferingQuantificationSteps.step3.bloc6.agony'),
      pain: t('MethodologyPage.sufferingQuantificationSteps.step3.bloc6.pain'),
      suffering: t('MethodologyPage.sufferingQuantificationSteps.step3.bloc6.suffering'),
      discomfort: t('MethodologyPage.sufferingQuantificationSteps.step3.bloc6.discomfort'),
    },
    {
      title: t('MethodologyPage.sufferingQuantificationSteps.step3.bloc7.title'),
      percent: '2,5%',
      text: t('MethodologyPage.sufferingQuantificationSteps.step3.text1'),
      agony: t('MethodologyPage.sufferingQuantificationSteps.step3.bloc7.agony'),
      pain: t('MethodologyPage.sufferingQuantificationSteps.step3.bloc7.pain'),
      suffering: t('MethodologyPage.sufferingQuantificationSteps.step3.bloc7.suffering'),
      discomfort: t('MethodologyPage.sufferingQuantificationSteps.step3.bloc7.discomfort'),
    },
    {
      title: t('MethodologyPage.sufferingQuantificationSteps.step3.bloc8.title'),
      percent: '0,225%',
      text: t('MethodologyPage.sufferingQuantificationSteps.step3.text1'),
      agony: t('MethodologyPage.sufferingQuantificationSteps.step3.bloc8.agony'),
      pain: t('MethodologyPage.sufferingQuantificationSteps.step3.bloc8.pain'),
      suffering: t('MethodologyPage.sufferingQuantificationSteps.step3.bloc8.suffering'),
      discomfort: t('MethodologyPage.sufferingQuantificationSteps.step3.bloc8.discomfort'),
    },
    {
      title: t('MethodologyPage.sufferingQuantificationSteps.step3.bloc9.title'),
      percent: '0,135%',
      text: t('MethodologyPage.sufferingQuantificationSteps.step3.text1'),
      agony: t('MethodologyPage.sufferingQuantificationSteps.step3.bloc9.agony'),
      pain: t('MethodologyPage.sufferingQuantificationSteps.step3.bloc9.pain'),
      suffering: t('MethodologyPage.sufferingQuantificationSteps.step3.bloc9.suffering'),
      discomfort: t('MethodologyPage.sufferingQuantificationSteps.step3.bloc9.discomfort'),
    },
    {
      title: t('MethodologyPage.sufferingQuantificationSteps.step3.bloc10.title'),
      percent: '0,035%',
      text: t('MethodologyPage.sufferingQuantificationSteps.step3.text1'),
      agony: t('MethodologyPage.sufferingQuantificationSteps.step3.bloc10.agony'),
      pain: t('MethodologyPage.sufferingQuantificationSteps.step3.bloc10.pain'),
      suffering: t('MethodologyPage.sufferingQuantificationSteps.step3.bloc10.suffering'),
      discomfort: t('MethodologyPage.sufferingQuantificationSteps.step3.bloc10.discomfort'),
    },
    {
      title: t('MethodologyPage.sufferingQuantificationSteps.step3.bloc11.title'),
      percent: '1,425%',
      text: t('MethodologyPage.sufferingQuantificationSteps.step3.text1'),
      agony: t('MethodologyPage.sufferingQuantificationSteps.step3.bloc11.agony'),
      pain: t('MethodologyPage.sufferingQuantificationSteps.step3.bloc11.pain'),
      suffering: t('MethodologyPage.sufferingQuantificationSteps.step3.bloc11.suffering'),
      discomfort: t('MethodologyPage.sufferingQuantificationSteps.step3.bloc11.discomfort'),
    },
    {
      title: t('MethodologyPage.sufferingQuantificationSteps.step3.bloc12.title'),
      percent: '5%',
      text: t('MethodologyPage.sufferingQuantificationSteps.step3.text1'),
      agony: t('MethodologyPage.sufferingQuantificationSteps.step3.bloc12.agony'),
      pain: t('MethodologyPage.sufferingQuantificationSteps.step3.bloc12.pain'),
      suffering: t('MethodologyPage.sufferingQuantificationSteps.step3.bloc12.suffering'),
      discomfort: t('MethodologyPage.sufferingQuantificationSteps.step3.bloc12.discomfort'),
    },
    {
      title: t('MethodologyPage.sufferingQuantificationSteps.step3.bloc13.title'),
      percent: '12,5%',
      text: t('MethodologyPage.sufferingQuantificationSteps.step3.text1'),
      agony: t('MethodologyPage.sufferingQuantificationSteps.step3.bloc13.agony'),
      pain: t('MethodologyPage.sufferingQuantificationSteps.step3.bloc13.pain'),
      suffering: t('MethodologyPage.sufferingQuantificationSteps.step3.bloc13.suffering'),
      discomfort: t('MethodologyPage.sufferingQuantificationSteps.step3.bloc13.discomfort'),
    },
    {
      title: t('MethodologyPage.sufferingQuantificationSteps.step3.bloc14.title'),
      percent: '100%',
      text: t('MethodologyPage.sufferingQuantificationSteps.step3.text1'),
      agony: t('MethodologyPage.sufferingQuantificationSteps.step3.bloc14.agony'),
      pain: t('MethodologyPage.sufferingQuantificationSteps.step3.bloc14.pain'),
      suffering: t('MethodologyPage.sufferingQuantificationSteps.step3.bloc14.suffering'),
      discomfort: t('MethodologyPage.sufferingQuantificationSteps.step3.bloc14.discomfort'),
    },
    {
      title: t('MethodologyPage.sufferingQuantificationSteps.step3.bloc15.title'),
      percent: '100%',
      text: t('MethodologyPage.sufferingQuantificationSteps.step3.text1'),
      agony: t('MethodologyPage.sufferingQuantificationSteps.step3.bloc15.agony'),
      pain: t('MethodologyPage.sufferingQuantificationSteps.step3.bloc15.pain'),
      suffering: t('MethodologyPage.sufferingQuantificationSteps.step3.bloc15.suffering'),
      discomfort: t('MethodologyPage.sufferingQuantificationSteps.step3.bloc15.discomfort'),
    },
    {
      title: t('MethodologyPage.sufferingQuantificationSteps.step3.bloc16.title'),
      percent: '100%',
      text: t('MethodologyPage.sufferingQuantificationSteps.step3.text1'),
      agony: t('MethodologyPage.sufferingQuantificationSteps.step3.bloc16.agony'),
      pain: t('MethodologyPage.sufferingQuantificationSteps.step3.bloc16.pain'),
      suffering: t('MethodologyPage.sufferingQuantificationSteps.step3.bloc16.suffering'),
      discomfort: t('MethodologyPage.sufferingQuantificationSteps.step3.bloc16.discomfort'),
    },
    {
      title: t('MethodologyPage.sufferingQuantificationSteps.step3.bloc17.title'),
      percent: '100%',
      text: t('MethodologyPage.sufferingQuantificationSteps.step3.text1'),
      agony: t('MethodologyPage.sufferingQuantificationSteps.step3.bloc17.agony'),
      pain: t('MethodologyPage.sufferingQuantificationSteps.step3.bloc17.pain'),
      suffering: t('MethodologyPage.sufferingQuantificationSteps.step3.bloc17.suffering'),
      discomfort: t('MethodologyPage.sufferingQuantificationSteps.step3.bloc17.discomfort'),
    },
    {
      title: t('MethodologyPage.sufferingQuantificationSteps.step3.bloc18.title'),
      percent: '0,01%',
      text: t('MethodologyPage.sufferingQuantificationSteps.step3.text1'),
      agony: t('MethodologyPage.sufferingQuantificationSteps.step3.bloc18.agony'),
      pain: t('MethodologyPage.sufferingQuantificationSteps.step3.bloc18.pain'),
      suffering: t('MethodologyPage.sufferingQuantificationSteps.step3.bloc18.suffering'),
      discomfort: t('MethodologyPage.sufferingQuantificationSteps.step3.bloc18.discomfort'),
    },
    {
      title: t('MethodologyPage.sufferingQuantificationSteps.step3.bloc19.title'),
      percent: '1,1%',
      text: t('MethodologyPage.sufferingQuantificationSteps.step3.text1'),
      agony: t('MethodologyPage.sufferingQuantificationSteps.step3.bloc19.agony'),
      pain: t('MethodologyPage.sufferingQuantificationSteps.step3.bloc19.pain'),
      suffering: t('MethodologyPage.sufferingQuantificationSteps.step3.bloc19.suffering'),
      discomfort: t('MethodologyPage.sufferingQuantificationSteps.step3.bloc19.discomfort'),
    },
    {
      title: t('MethodologyPage.sufferingQuantificationSteps.step3.bloc20.title'),
      percent: '100%',
      text: t('MethodologyPage.sufferingQuantificationSteps.step3.text1'),
      agony: t('MethodologyPage.sufferingQuantificationSteps.step3.bloc20.agony'),
      pain: t('MethodologyPage.sufferingQuantificationSteps.step3.bloc20.pain'),
      suffering: t('MethodologyPage.sufferingQuantificationSteps.step3.bloc20.suffering'),
      discomfort: t('MethodologyPage.sufferingQuantificationSteps.step3.bloc20.discomfort'),
    },
  ];

  return (
    <div className="max-w-[1066px]">
      <div className="flex flex-col md:flex-row gap-6">
        <hgroup className="w-full md:w-1/2">
          <h2 className="text-2xl font-extrabold mb-4 uppercase ">
            {t('MethodologyPage.QuantifySufferingByPain.global_suffering_figure_sectinon.title')}
          </h2>
          <p className="text-md mb-6 font-bold">
            {t('MethodologyPage.QuantifySufferingByPain.global_suffering_figure_sectinon.question')}
          </p>
          <p className="text-md">
            {t('MethodologyPage.QuantifySufferingByPain.global_suffering_figure_sectinon.description1')}
          </p>
          <p className="text-md mb-2">
            {t('MethodologyPage.QuantifySufferingByPain.global_suffering_figure_sectinon.description2')}
          </p>
        </hgroup>

        <article className="flex-1">
          <AnimatedAfflictionsGroup afflictions={afflictions} delay={4000} cascade={300} />{' '}
          <p className="bg-white text-caption uppercase rounded-[5px] p-4 my-2">
            {t('MethodologyPage.sufferingQuantificationSteps.step3.text2')}
          </p>
          <p className="bg-violet rounded-[5px] text-center text-3xl p-2 my-4 font-extrabold">=</p>
          {/* Synthèse */}
          <div className="bg-white rounded-[5px] p-4">
            <h5 className="mb-2">{t('MethodologyPage.sufferingQuantificationSteps.step3.result.title')}</h5>
            <div className="w-full grid grid-cols-2 grid-rows-2 normal-case text-center">
              <SufferingScales
                agony_duration_text={t('MethodologyPage.sufferingQuantificationSteps.step3.result.agony')}
                pain_duration_text={t('MethodologyPage.sufferingQuantificationSteps.step3.result.pain')}
                suffering_duration_text={t('MethodologyPage.sufferingQuantificationSteps.step3.result.suffering')}
                discomfort_duration_text={t('MethodologyPage.sufferingQuantificationSteps.step3.result.suffering')}
              />
            </div>
          </div>
        </article>
      </div>
    </div>
  );
}
