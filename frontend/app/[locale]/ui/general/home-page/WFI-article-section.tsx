import { getScopedI18n } from '@/locales/server';
import Image from 'next/image';

export default async function WFIArticleSection() {
  const scopedT = await getScopedI18n('WFIArticle');

  return (
    <section className=" min-h-screen p-8 sm:px-16 w-full bg-[#E7E4FF] flex flex-col gap-5">
      <h1 className="w-full text-3xl lg:text-5xl font-bold text-[#3b0a0a] text-left">
        {scopedT('title.part1')}
        <span className="text-[#ff7f7f]">&nbsp;{scopedT('title.strong1')}</span>
        &nbsp;{scopedT('title.part2')}
        <br />
        {scopedT('title.part3')}
        <span className="text-[#ff7f7f]">&nbsp;{scopedT('title.strong2')}</span>.
      </h1>

      <figure className="w-full flex items-center justify-between gap-5 flex-col lg:flex-row ">
        <Image
          src="/wfi_article_figure.png"
          width={560}
          height={620}
          className="block"
          alt="Picture of a WFI researchers"
        />
        <figcaption className="max-w-xl ">
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

      <article className="flex justify-between text-[#3b0a0a] font-extrabold tracking-wide lg:flex-row flex-wrap">
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
