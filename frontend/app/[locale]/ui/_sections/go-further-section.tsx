import { getI18n } from '@/locales/server';
import BrevoNewsletterForm from '../_components/BrevoNewsletterForm';
import SectionTitle from '../../home/_components/section-title';

export default async function GoFurtherSection() {
  const t = await getI18n();

  return (
    <section
      id="GoFurtherSection"
      className=" p-section flex flex-col items-center justify-center bg-black text-center "
      aria-labelledby="go-further-heading"
    >
      <div className="max-w-contain">
        <SectionTitle image_path="free_hen_egg.svg" image_alt="" title={t('GoFurther.title')} text_color="white" />
        <div className="flex flex-col gap-[24px] items-center justify-center mt-4">
          <p id="go-further-heading" className="lead text-grey max-w-[800px]">
            {t('GoFurther.subtitle')}
          </p>
          <div>
            <BrevoNewsletterForm />
          </div>
        </div>
      </div>
    </section>
  );
}
