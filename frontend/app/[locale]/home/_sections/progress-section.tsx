import { getI18n } from '@/locales/server';
import ContentWithImageSection from '@/app/[locale]/home/_components/content-with-image-component';
import SectionTitle from '../_components/section-title';

export default async function ProgressSection() {
  const t = await getI18n();

  return (
    <section
      id="ProgressSection"
      className="min-h-screen py-8 w-full max-w-screen-xl mx-auto px-4 scroll-mt-18 flex flex-col justify-center items-center"
      aria-labelledby="results-heading"
    >
      <SectionTitle image_path="/half-bars_egg.svg" image_alt="" title={t('ProgressSection.title').toUpperCase()} />
      <div className="flex flex-col justify-center items-center">
        <div className="w-full md:5/6 lg:w-4/6 flex flex-col gap-7">
          <ContentWithImageSection
            text_heading={t('ProgressSection.more_than_80_percent_without_cage')}
            text_content={t('ProgressSection.from_70_percent_in_2015_to_less_than_20_percent')}
            image_url="progress_bluegraph.svg"
            image_description={''} //TODO
            image_position="left"
          />
          <ContentWithImageSection
            text_heading={t('ProgressSection.most_supermarkets_still_sell_caged_eggs')}
            text_content={t('ProgressSection.survey_results_2026')}
            image_url="progress_redgraph.svg"
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
