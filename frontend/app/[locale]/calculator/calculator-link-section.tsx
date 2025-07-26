import { getScopedI18n } from '@/locales/server';
import Image from 'next/image';
import Link from 'next/link';

export default async function CalculatorLinkSection() {
  const scopedT = await getScopedI18n('calculatorPage');

  return (
    <section className="bg-pink-1 flex items-center flex-col gap-5 m-16 py-10">
      <h1 className=" w-full text-3xl lg:text-5xl font-bold dark-text text-center text-wrap">
        {scopedT('linkSection')}
      </h1>
      <Link
        target="_blank"
        href="https://fr.openfoodfacts.org/cgi/search.pl?search_terms=boites+d%27oeufs&search_simple=1&action=process"
        className="w-85 max-w-3/4 text-center bg-white font-mono font-bold py-1 px-2 rounded-full shadow-[4px_4px_0_#000] hover:shadow-[0px_3px_8px_#000000] flex items-center justify-center transition-all duration-200 overflow-hidden"
        aria-label={scopedT('descriptionSection.imageAlt')}
      >
        <Image
          src="/off-logo-horizontal-light.svg"
          width={540}
          height={740}
          alt={scopedT('descriptionSection.imageAlt')}
          className="bg-white block p-2 "
        />
      </Link>
    </section>
  );
}
