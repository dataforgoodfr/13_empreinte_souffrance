import { getScopedI18n } from '@/locales/server';
import Image from 'next/image';

export default async function WFIArticleSection() {
  const scopedT = await getScopedI18n('WFIArticle');

  return (
    <section
      id="WFIArticleSection"
      className="scroll-mt-18 max-w-screen  p-8 sm:px-16 w-full bg-[#E7E4FF] flex flex-col gap-16"
    >
      <h1 className="w-full text-3xl lg:text-5xl font-bold text-[#3b0a0a] text-left">
        {scopedT('title.part1')}
        <span className="text-[#ff7f7f]">&nbsp;{scopedT('title.strong1')}</span>
        &nbsp;{scopedT('title.part2')}
        <br />
        {scopedT('title.part3')}
        <span className="text-[#ff7f7f]">&nbsp;{scopedT('title.strong2')}</span>.
      </h1>

      <figure className="w-full flex  items-stretch justify-between flex-col lg:flex-row gap-5">
        <div className="relative md:basis-2/3  basis-1/3 min-w-0 2xl:h-[500px] h-[400px] flex items-start justify-start">
          <Image
            src="/wfi_article_figure.png"
            alt="Picture of a WFI researchers"
            fill
            className="object-contain object-left"
            sizes="(max-width: 1024px) 100vw, 66vw"
            priority
          />
        </div>
        <figcaption className=" md:basis-1/3 basis-2/3 max-w-full flex-shrink-0 self-center">
          <p className="text-2xl text-[#3b0a0a]">
            {scopedT('description.part0')}
            &nbsp;<strong>{scopedT('description.strong1')}</strong>
            &nbsp;{scopedT('description.part1')}
            <br />
            <br />
            {scopedT('description.part2')}
          </p>
        </figcaption>
      </figure>

      <article className="flex justify-between text-[#3b0a0a] font-extrabold tracking-wide lg:flex-row flex-wrap w-full">
        <hgroup>
          <h2 className="bg-white text-center text-3xl sm:text-4xl flex justify-start items-center w-fit">500+</h2>
          <h3>{scopedT('key_number.key1')}</h3>
        </hgroup>
        <hgroup>
          <h2 className="bg-white text-center text-3xl sm:text-4xl flex justify-start items-center w-fit ">
            4 {scopedT('key_number.years')}
          </h2>
          <h3>{scopedT('key_number.key2')}</h3>
        </hgroup>
        <hgroup>
          <h2 className="bg-white text-center text-3xl sm:text-4xl flex justify-start items-center w-fit">50+</h2>
          <h3>{scopedT('key_number.key3')}</h3>
        </hgroup>
        <hgroup>
          <h2 className="bg-white text-center text-3xl sm:text-4xl flex justify-start items-center w-fit ">1</h2>
          <h3>{scopedT('key_number.key4')}</h3>
        </hgroup>
      </article>
    </section>
  );
}
