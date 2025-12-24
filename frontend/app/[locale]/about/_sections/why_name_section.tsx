import { getScopedI18n } from '@/locales/server';
import SectionTitle from '../../home/_components/section-title';

export default async function WhyNameSection() {
  const scopedT = await getScopedI18n('aboutPage.whyNameSection');

  return (
    <section className="p-section flex justify-center bg-violet text-black">
      <div className="max-w-contain ">
        <figure className="flex flex-col items-center gap-6">
          <SectionTitle
            image_path="/full-bars_egg.svg"
            image_alt="icon of an egg behind bars"
            title={scopedT('why_welfare_footprint_title').toUpperCase()}
          />

          <figcaption className="flex flex-col items-center gap-6 max-w-[650px]">
            <div className="flex flex-col gap-3">
              <p>{scopedT('why_welfare_footprint_description.main_description')}</p>
              <p>{scopedT('why_welfare_footprint_description.goals')}</p>
              <p>{scopedT('why_welfare_footprint_description.engagement_assessment')}</p>
              <p>{scopedT('why_welfare_footprint_description.invisible_eggs')}</p>
              <p>{scopedT('why_welfare_footprint_description.store_actions')}</p>
            </div>
          </figcaption>
        </figure>
      </div>
    </section>
  );
}
