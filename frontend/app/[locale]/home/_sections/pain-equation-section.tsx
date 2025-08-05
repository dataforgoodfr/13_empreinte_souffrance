import { getI18n } from '@/locales/server';
import Link from 'next/link';
import SectionHeading from '@/app/[locale]/ui/_sections/section-heading';
import SufferingStagesDescription from '@/app/[locale]/ui/_components/suffering-stages-description';

export default async function PainEquationSection() {
  const t = await getI18n();

  return (
    <section
      id="PainEquationSection"
      aria-labelledby="pain-equation-title"
      className="py-16 px-4 bg-white scroll-mt-18"
    >
      <div className="max-w-screen-xl mx-auto px-4">
        <SectionHeading title={t('PainEquationSection.title')} heading_number="2" />

        <div className="max-w-screen-xl mx-auto px-4">
          <div className="mt-8 w-full flex flex-col md:grid md:grid-cols-3 items-center text-center border border-black divide-y md:divide-y-0 md:divide-x divide-black font-extrabold text-xl">
            <div className="py-2 w-full">{t('PainEquationSection.formula.duration')}</div>
            <div className="py-2 w-full">{t('PainEquationSection.formula.intensity')}</div>
            <div className="py-2 w-full">{t('PainEquationSection.formula.burden')}</div>{' '}
          </div>

          <p className="mt-12 mb-12 max-w-2xl mx-auto text-center sm:text-lg">{t('PainEquationSection.description')}</p>

          <section aria-labelledby="pain-stages" className="mb-12">
            <h3 id="pain-stages" className="sr-only">
              {t('PainEquationSection.painStagesLabel')}
            </h3>

            <SufferingStagesDescription />

            <footer className="text-center mt-8">
              <Link
                href="/methodology"
                className="inline-block border-[0.1px] border-pink-3 py-3 px-6 text-lg hover:bg-(--violet-1)  w-full font-mono dark-text tracking-wider transition-all duration-200 "
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
