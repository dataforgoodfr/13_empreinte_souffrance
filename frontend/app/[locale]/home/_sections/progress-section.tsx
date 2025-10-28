import { getI18n } from '@/locales/server';
import ContentWithImageSection from '@/app/[locale]/home/_components/content-with-image-component';
import SectionHeading from '@/app/[locale]/ui/_sections/section-heading';

export default async function ProgressSection() {
  const t = await getI18n();

  return (
    <section
      id="ProgressSection"
      className="min-h-screen py-8 w-full max-w-screen-xl mx-auto px-4 scroll-mt-18"
      aria-labelledby="results-heading"
    >
      <SectionHeading title={t('Results.title')} heading_number="3" />
      <div className="flex flex-col justify-center items-center">
        <div className="w-full md:5/6 lg:w-4/6 flex flex-col gap-7">
          <ContentWithImageSection
            text_heading={t('Results.agony.title')}
            text_content={t('Results.agony.content')}
            image_url="progress_bluegraph.png"
            image_description={t('Results.agony.image_description')}
            image_position="left"
          />
          <ContentWithImageSection
            text_heading={t('Results.discomfort.title')}
            text_content={t('Results.discomfort.content')}
            image_url="progress_redgraph.png"
            image_description={t('Results.discomfort.image_description')}
            image_position="right"
          />
          <ContentWithImageSection
            text_heading={t('Results.suffering_reduction.title')}
            text_content={t('Results.suffering_reduction.content')}
            image_url="progress_bakery.jpg"
            image_description={t('Results.suffering_reduction.image_description')}
            image_position="left"
          />
        </div>
      </div>
    </section>
  );
}
