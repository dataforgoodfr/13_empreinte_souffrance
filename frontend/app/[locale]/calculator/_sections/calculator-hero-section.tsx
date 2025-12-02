import { getScopedI18n } from '@/locales/server';
import Image from 'next/image';

export default async function CalculatorHeroSection() {
  const scopedT = await getScopedI18n('calculatorPage');
  return (
    <section className="p-section flex justify-center ">
      <div className='max-w-contain'>

      
      <h1 className="w-full md:w-1/2 font-bold text-brown text-left uppercase">
        {scopedT('descriptionSection.title')}
      </h1>
      <figure className="flex flex-col md:flex-row justify-evenly items-center gap-16">
        <Image
          src="/eggs_box.jpeg"
          width={540}
          height={740}
          alt={scopedT('descriptionSection.imageAlt')}
          className="w-full md:w-1/2"
        />

        <figcaption className="flex justify-center items-center ">
          <p className="w-full md:w-2/3 text-bold text-brown text-lead ">{scopedT('descriptionSection.figcaption')}</p>
        </figcaption>
      </figure>
      </div>
    </section>
  );
}
