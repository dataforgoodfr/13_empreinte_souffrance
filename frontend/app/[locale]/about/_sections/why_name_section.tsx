import { getScopedI18n } from '@/locales/server';
import Image from 'next/image';

export default async function WhyNameSection() {
  const scopedT = await getScopedI18n('aboutPage.whyNameSection');

  return (
    <section className="p-section flex flex-col items-center bg-violet text-black">
      <figure>
        <Image
          src="/full-bars_egg.svg"
          width={200}
          height={200}
          alt="egg shaped logo with a hen behind bars"
          className="mb-0 md:mb-0"
        />
      </figure>

      <figcaption className='flex flex-col items-center gap-[20px]'>
        <h2 className="lg:max-w-[550px] text-center">{scopedT('why_welfare_footprint_title')}</h2>
        <div className="flex flex-col gap-[10px] lg:max-w-1/3">
          <p>{scopedT('why_welfare_footprint_description.new_scientific_work')}</p>
          <p>{scopedT('why_welfare_footprint_description.accessible_result')}</p>
          <p>{scopedT('why_welfare_footprint_description.firm_engagement')}</p>
          <p>{scopedT('why_welfare_footprint_description.decisive_moment')}</p>
        </div>
      </figcaption>
    </section>
  );
}
