import { getScopedI18n } from '@/locales/server';
import Image from 'next/image';

export default async function WhyNameSection() {
  const scopedT = await getScopedI18n('aboutPage.whyNameSection');

  return (
    <section className="p-section flex justify-center bg-violet text-black">
      <div className="max-w-contain ">
        <figure className="flex flex-col md:flex-row items-center">
          <Image
            src="/full-bars_egg.svg"
            width={800}
            height={800}
            alt={'icon of an egg behind bars'}
            className=" mb-0 md:mb-0 min-w-2/5"
          />

          <figcaption className="flex flex-col items-start gap-6 min-w-[3/5]">
            <h3>{scopedT('why_welfare_footprint_title').toUpperCase()}</h3>
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
