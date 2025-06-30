import { getI18n } from '@/locales/server';
import { AnimatedAfflictionsGroup } from './animated-afflictions';

export default async function GlobalSufferingFigure() {
  const t = await getI18n();

  //todo! add more afflictions
  const afflictions = [
    {
      title: t('MethodologyPage.sufferingQuantificationSteps.step3.bloc1.title'),
      percent: '33%',
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
    // ... add more afflictions here !
  ];

  return (
    <section className="max-w-screen-xl mx-auto ">
      <div className="sm:px-6 pb-20 xl:px-0 p-6 gap-4 flex flex-col md:flex-row w-full ">
        <div className="flex flex-col md:w-1/2  sm:p-20 lg:p-6  mx-auto ">
          <h2 className="text-2xl font-extrabold mb-4 uppercase ">
            2.3 Chiffrer la souffrance globale d’une poule d’élevage
          </h2>
          <p className="text-md mb-6">
            Comment combiner fractures, infections, stress... pour obtenir une mesure unique de la souffrance ?
          </p>
          <p className="text-md">
            Les étapes précédentes ont permis de connaître les sources de douleur pour les poules, leur fréquence et la
            quantité de souffrance associée à chacune .
          </p>
          <p className="text-md mb-2">
            Il reste à faire la somme de tous ces résultats pour déterminer la souffrance globale subie par une poule.
          </p>
        </div>

        <article className="flex-1 md:basis-1/3 divide-y divide-[#FF7B7B] border border-[#FF7B7B] mx-2">
          <AnimatedAfflictionsGroup afflictions={afflictions} delay={4000} cascade={300} />{' '}
          <div className="normal-case p-2 text-xs">{t('MethodologyPage.sufferingQuantificationSteps.step3.text2')}</div>
          <div className="bg-[#E7E4FF] text-center text-3xl font-extrabold">=</div>
          <div className="bg-white p-4">
            <h3 className="text-xs font-extrabold mb-2">
              {t('MethodologyPage.sufferingQuantificationSteps.step3.bloc5.title')}
            </h3>
            <div className="text-[9px] normal-case mx-auto">
              <div className="grid grid-cols-2 grid-rows-2 text-xs font-normal text-left normal-case mx-auto">
                <div className="bg-[#3C1212] text-white p-2">
                  {t('MethodologyPage.sufferingQuantificationSteps.step3.bloc5.agony')}
                </div>
                <div className="bg-[#FF7B7B] text-[#3C1212] p-2">
                  {t('MethodologyPage.sufferingQuantificationSteps.step3.bloc5.pain')}
                </div>
                <div className="bg-[#FFC3C3] text-[#3C1212] p-2">
                  {t('MethodologyPage.sufferingQuantificationSteps.step3.bloc5.suffering')}
                </div>
                <div className="bg-[#FFE9E9] text-[#3C1212] p-2">
                  {t('MethodologyPage.sufferingQuantificationSteps.step3.bloc5.discomfort')}
                </div>
              </div>
            </div>
          </div>
        </article>
      </div>
    </section>
  );
}
