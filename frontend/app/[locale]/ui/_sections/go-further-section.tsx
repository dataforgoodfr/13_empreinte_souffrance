import { getI18n } from '@/locales/server';
import Link from 'next/link';
import BrevoNewsletterForm from '../_components/BrevoNewsletterForm';

export default async function GoFurtherSection() {
  const t = await getI18n();

  return (
    <section
      id="GoFurtherSection"
      className="flex flex-col items-center justify-center p-section bg-black text-center "
      aria-labelledby="go-further-heading"
    >
      <img src="/free-hen-icon.png" className="w-[150px]" />

      <div className="flex flex-col gap-[24px] items-center justify-center">
        <h2 id="go-further-heading" className="text-h2 md:text-h2-desktop font-extrabold text-grey max-w-[605px]">
          {t('GoFurther.title')}
        </h2>
        <p id="go-further-heading" className="text-grey text-bold max-w-[800px]">
          {t('GoFurther.subtitle')}
        </p>

        <div className="flex flex-col md:flex-row flex-wrap gap-6 justify-center items-center w-full md:max-w-[80dvw]">
          <Link
            href="/"
            target="_blank"
            className="primary-button min-w-[30dvw] w-full md:max-w-[30dvw]"
            aria-label={t('GoFurther.signPetition')}
          >
            {t('GoFurther.signPetition')}
          </Link>
          <Link
            href="/"
            target="_blank"
            className="primary-button min-w-[30dvw] w-full md:max-w-[30dvw]"
            aria-label={t('GoFurther.goEvent')}
          >
            {t('GoFurther.goEvent')}
          </Link>
        </div>
        <div>
          <Link
            href="/"
            target="_blank"
            className="secondary-button min-w-[30dvw] w-full md:max-w-[30dvw]"
            aria-label={t('GoFurther.share')}
          >
            {t('GoFurther.share')}
          </Link>
          <BrevoNewsletterForm />
        </div>
      </div>
    </section>
  );
}
