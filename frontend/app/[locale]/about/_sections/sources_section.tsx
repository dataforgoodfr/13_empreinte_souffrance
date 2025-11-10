import { getScopedI18n } from '@/locales/server';


export default async function SourcesSection() {
     const scopedT = await getScopedI18n("aboutPage");


  return (
    <section className='p-section flex flex-col items-center justify-center bg-grey text-black gap-[28px]'>
      <h1>SOURCES</h1>
      <p className='lg:max-w-2/3 body'>section placeholer</p>
    </section>
  );
}
