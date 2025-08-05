import { getScopedI18n } from '@/locales/server';

export default async function ThankingSection() {
     const scopedT = await getScopedI18n("aboutPage");

  return (
    <section className='section-padding flex justify-center  bg-violet-1'>
      <p className='lg:max-w-2/3 body'>{scopedT('thanking_section')}</p>
    </section>
  );
}
