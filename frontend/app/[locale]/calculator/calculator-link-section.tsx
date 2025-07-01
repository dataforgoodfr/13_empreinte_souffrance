import { getScopedI18n } from '@/locales/server';
import Image from 'next/image';

export default async function CalculatorLinkSection() {
  const scopedT = await getScopedI18n('calculatorPage');

  return (
    <section className="flex items-center flex-col gap-5 m-16">
      <h1 className=" w-full text-3xl lg:text-5xl font-bold text-[#3b0a0a] text-center text-wrap">
        {scopedT('linkSection')}
      </h1>
      <a
        target="_blank"
        href="https://fr.openfoodfacts.org/cgi/search.pl?search_terms=boites+d%27oeufs&search_simple=1&action=process"
      >
        <Image
          src="/off-logo-horizontal-light.svg"
          width={540}
          height={740}
          alt={scopedT('descriptionSection.imageAlt')}
          className="bg-white block p-2 hover:shadow-[0px_3px_8px_#000000]"
        />
      </a>
    </section>
  );
}
