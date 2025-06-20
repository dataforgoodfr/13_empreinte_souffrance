import { getScopedI18n } from '@/locales/server';


export default async function CallToActionSection() {
  const scopedT = await getScopedI18n('calculatorPage');
  return (
    <section className="scroll-mt-18 max-w-screen  p-8 sm:px-16 w-full bg-white flex flex-col gap-16">
     
      <h2 className="w-full text-3xl lg:text-5xl font-bold text-[#3b0a0a] text-left">{scopedT('descriptionSection.title')}</h2>
     
      <article className="flex justify-between text-[#3b0a0a] font-extrabold tracking-wide lg:flex-row flex-wrap w-full">
        <hgroup>
          <h2 className="bg-white text-center text-3xl sm:text-4xl flex justify-start items-center w-fit">500+</h2>
          <h3>{scopedT('calculSection.keySection.key1')}</h3>
        </hgroup>
        <hgroup>
          <h2 className="bg-white text-center text-3xl sm:text-4xl flex justify-start items-center w-fit ">
            4 {scopedT('calculSection.keySection.key1')}
          </h2>
          <h3>{scopedT('calculSection.keySection.key2')}</h3>
        </hgroup>
        <hgroup>
          <h2 className="bg-white text-center text-3xl sm:text-4xl flex justify-start items-center w-fit">50+</h2>
          <h3>{scopedT('calculSection.keySection.key3')}</h3>
        </hgroup>
        <hgroup>
          <h2 className="bg-white text-center text-3xl sm:text-4xl flex justify-start items-center w-fit ">1</h2>
          <h3>{scopedT('calculSection.keySection.key4')}</h3>
        </hgroup>
      </article>
    </section>
  );
}
