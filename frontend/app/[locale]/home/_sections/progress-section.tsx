import { getI18n } from '@/locales/server';
import ContentWithImageSection from '@/app/[locale]/home/_components/content-with-image-component';
import Image from 'next/image';

export default async function ProgressSection() {
  const t = await getI18n();

  return (
    <section
      id="ProgressSection"
      className="min-h-screen py-8 w-full max-w-screen-xl mx-auto px-4 scroll-mt-18 flex flex-col justify-center items-center"
      aria-labelledby="results-heading"
    >
      <Image src="half-bars_egg.svg" width={150} height={250} alt={'TMP egg progress bars'} className="block p-2" />
      <h1
        id="results-heading"
        className="text-black flex flex-col justify-center md:flex-row md:justify-start text-left md:text-center items-center gap-8 mb-8"
      >
        {t('ProgressSection.title').toUpperCase()}
      </h1>
      <div className="flex flex-col justify-center items-center">
        <div className="w-full md:5/6 lg:w-4/6 flex flex-col gap-7">
          <ContentWithImageSection
            text_heading={t('ProgressSection.more_than_80_percent_without_cage')}
            text_content={t('ProgressSection.from_70_percent_in_2015_to_less_than_20_percent')}
            image_url="progress_bluegraph.png"
            image_description={''} //TODO
            image_position="left"
          />
          <ContentWithImageSection
            text_heading={t('ProgressSection.most_supermarkets_still_sell_caged_eggs')}
            text_content={t('ProgressSection.survey_results_2026')}
            image_url="progress_redgraph.png"
            image_description={''} //TODO
            image_position="right"
          />
          <ContentWithImageSection
            text_heading={t('ProgressSection.no_transparency_for_ingredients')}
            text_content={t('ProgressSection.only_35_percent_display_no_caged_eggs')}
            image_url="progress_bakery.jpg"
            image_description={''} //TODO
            image_position="left"
          />
        </div>
      </div>
    </section>
  );
}
