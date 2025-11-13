import { getScopedI18n } from '@/locales/server';
import Image from 'next/image';
import Link from 'next/link';

export default async function CalculatorLinkSection() {
  const scopedT = await getScopedI18n('calculatorPage');

  return (
    <section className="bg-pink-1 p-section flex justify-center">
      <div className="flex flex-col items-center justify-center gap-6 w-[900px]">
        <Image
          src="/loupe_icon.png"
          width={74}
          height={74}
          alt={scopedT('descriptionSection.imageAlt')}
          className=" block p-2 "
        />
        <h2 className="font-bold text-brown text-center text-wrap uppercase">{scopedT('linkSection')}</h2>

        <Link
          target="_blank"
          href="https://fr.openfoodfacts.org/cgi/search.pl?search_terms=boites+d%27oeufs&search_simple=1&action=process"
          className="tertiary-button flex justify-center"
          aria-label={scopedT('descriptionSection.imageAlt')}
        >
          <Image
            src="/off-logo-horizontal-light.svg"
            width={350}
            height={250}
            alt={scopedT('descriptionSection.imageAlt')}
            className=" "
          />
        </Link>
      </div>
    </section>
  );
}
