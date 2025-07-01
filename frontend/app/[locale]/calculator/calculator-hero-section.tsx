import { getScopedI18n } from '@/locales/server';
import Image from 'next/image';

export default async function CalculatorHeroSection() {
  const scopedT = await getScopedI18n('calculatorPage');
  return (

    <section className="scroll-mt-18 max-w-screen p-8 sm:px-16 w-full bg-white flex flex-col justify-center items center gap-16">
      <h1 className="w-full text-3xl lg:text-5xl font-bold text-[#3b0a0a] text-left uppercase">
        {scopedT('descriptionSection.title')}
      </h1>
      <figure className="flex justify-evenly w-full  flex-col sm:flex-row items-center">

        <Image
          src="/eggs_box.jpeg"
          width={540}
          height={740}
          alt={scopedT('descriptionSection.imageAlt')}
          className="block rounded w-2/4"
        />

        <figcaption className=" text-2xl flex w-full sm:w-1/3 items-center text-[#3b0a0a] ">
          {scopedT('descriptionSection.figcaption')}
        </figcaption>

      </figure>
    </section>
  );
}
