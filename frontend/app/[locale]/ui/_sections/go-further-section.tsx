import { getI18n } from '@/locales/server';
import Link from 'next/link';
import BrevoNewsletterForm from '../_components/BrevoNewsletterForm';
import SectionTitle from '../../home/_components/section-title';

export default async function GoFurtherSection() {
  const t = await getI18n();

  return (
    <section
      id="GoFurtherSection"
      className="flex flex-col items-center justify-center p-section bg-black text-center "
      aria-labelledby="go-further-heading"
    >
      <SectionTitle image_path="free_hen_egg.svg" image_alt="" title={t('GoFurther.title')} text_color="white" />
      <div className="flex flex-col gap-[24px] items-center justify-center">
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
