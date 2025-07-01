import { getI18n } from '@/locales/server';
import Link from 'next/link';
import SectionHeading from '@/app/[locale]/ui/general/home-page/elements/section-heading';

export default async function PainEquationSection() {
  const t = await getI18n();

  return (
    <section
      id="PainEquationSection"
      aria-labelledby="pain-equation-title"
      className="py-16 px-4  bg-white text-gray-900 scroll-mt-18"
    >
      <div className="max-w-screen-xl mx-auto px-4">
        <SectionHeading title={t('PainEquationSection.title')} heading_number="2" />

        <div className="max-w-screen-xl mx-auto px-4">
          <div className="mt-8 w-full flex flex-col md:grid md:grid-cols-3 items-center text-center border border-black divide-y md:divide-y-0 md:divide-x divide-black font-extrabold text-xl">
            <div className="py-2 w-full">{t('PainEquationSection.formula.duration')}</div>
            <div className="py-2 w-full">{t('PainEquationSection.formula.intensity')}</div>
            <div className="py-2 w-full">{t('PainEquationSection.formula.burden')}</div>{' '}
          </div>

          <p className="mt-12 mb-12 max-w-2xl mx-auto text-base text-center sm:text-lg">
            {t('PainEquationSection.description')}
          </p>

          <section aria-labelledby="pain-stages" className="mb-12">
            <h3 id="pain-stages" className="sr-only">
              {t('PainEquationSection.painStagesLabel')}
            </h3>

            <div className="grid grid-cols-1 md:grid-cols-4 ">
              <article className="bg-red-100 p-4 border border-red-200">
                <h4 className="font-bold uppercase mb-4 mt-4">{t('PainEquationSection.stages.discomfort.title')}</h4>
                <p className="text-sm font-medium">{t('PainEquationSection.stages.discomfort.text')}</p>
              </article>
              <article className="bg-red-200 p-4 border border-red-300">
                <h4 className="font-bold uppercase mb-4 mt-4">{t('PainEquationSection.stages.pain.title')}</h4>
                <p className="text-sm font-medium">{t('PainEquationSection.stages.pain.text')}</p>
              </article>
              <article className="bg-red-300 p-4 border border-red-400">
                <h4 className="font-bold uppercase mb-4 mt-4">{t('PainEquationSection.stages.suffering.title')}</h4>
                <p className="text-sm font-medium">{t('PainEquationSection.stages.suffering.text')}</p>
              </article>
              <article className="bg-red-900 text-white p-4 border border-red-700">
                <h4 className="font-bold uppercase mb-4 mt-4">{t('PainEquationSection.stages.agony.title')}</h4>
                <p className="text-sm font-medium">{t('PainEquationSection.stages.agony.text')}</p>
              </article>
            </div>

            <footer className="text-center mt-8">
              <Link
                href="/methodology"
                className="inline-block border-[0.1px] border-[#ff7f7f] py-3 px-6 text-lg hover:bg-gray-100  w-full font-mono text-[#3b0a0a] tracking-wider transition-all duration-200 "
                aria-label={t('PainEquationSection.cta')}
              >
                {t('PainEquationSection.cta')}
              </Link>
            </footer>
          </section>
        </div>
      </div>
    </section>
  );
}
