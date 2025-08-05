import { getScopedI18n } from '@/locales/server';

export default async function WhyNameSection() {
  const scopedT = await getScopedI18n('aboutPage.whyNameSection');

  return (
    <section className="section-padding flex flex-col gap-[20px] items-center  bg-brown text-pink-1">
      <figure className="flex flex-row gap-[15px]">
        <img src="/free_hens_logo.png" alt="free hens logo" />
        <img src="/caged_hens_logo.png" alt="caged hens logo" />
      </figure>

      <h2 className="lg:max-w-[550px] text-center">{scopedT('why_welfare_footprint_title')}</h2>
      <div className="flex flex-col gap-[10px] lg:max-w-1/3">
        <p>{scopedT('why_welfare_footprint_description.new_scientific_work')}</p>
        <p>{scopedT('why_welfare_footprint_description.accessible_result')}</p>
        <p>{scopedT('why_welfare_footprint_description.firm_engagement')}</p>
        <p>{scopedT('why_welfare_footprint_description.decisive_moment')}</p>
      </div>
    </section>
  );
}
