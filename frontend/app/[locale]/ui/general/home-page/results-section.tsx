import { getI18n } from '@/locales/server';
import ContentWithImageSection from '@/app/[locale]/ui/general/content-with-image-section';
import SectionHeading from '@/app/[locale]/ui/general/home-page/elements/section-heading';

export default async function ResultsSection() {
  const t = await getI18n();

  return (
    <section id="ResultSection" className="min-h-screen py-8 w-full max-w-screen-xl mx-auto px-4 scroll-mt-18" aria-labelledby="results-heading">
      <SectionHeading title={t('Results.title')} heading_number="3" />
      <div className="flex flex-col justify-center items-center">
        <div className="border-1 border-[#ff7f7f] w-full md:5/6 lg:w-4/6">
          <ContentWithImageSection
            text_heading={t('Results.agony.title')}
            text_content={t('Results.agony.content')}
            image_url="agony.png"
            image_description={t('Results.agony.image_description')}
            image_position="right"
          />
          <ContentWithImageSection
            text_heading={t('Results.discomfort.title')}
            text_content={t('Results.discomfort.content')}
            image_url="discomfort.png"
            image_description={t('Results.discomfort.image_description')}
            image_position="left"
          />
          <ContentWithImageSection
            text_heading={t('Results.suffering_reduction.title')}
            text_content={t('Results.suffering_reduction.content')}
            image_url="suffering_reduction.png"
            image_description={t('Results.suffering_reduction.image_description')}
            image_position="right"
          />
          <ContentWithImageSection
            text_heading={t('Results.cage_figure.title')}
            text_content={t('Results.cage_figure.content')}
            image_url="cage_figure.png"
            image_description={t('Results.cage_figure.image_description')}
            image_position="left"
          />
        </div>
      </div>
    </section>
  );
}
