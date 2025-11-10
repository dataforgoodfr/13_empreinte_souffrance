import { getScopedI18n } from '@/locales/server';
import Link from 'next/link';
import Image from 'next/image';

export default async function AssociationPresentationSection() {
  const scopedT = await getScopedI18n('aboutPage.association_presentation_section');

  return (
    <section className="p-section bg-white">
      <h1 className="mb-8 border md:max-w-2/3 text-brown">{scopedT('two_hens_out_five_title').toUpperCase()}</h1>
      <div className="flex flex-wrap lg:p-8 gap-8 justify-between">
        <div className="flex flex-col gap-5 max-w-[700px]">
          <Link href="https://animafrance.org/" target="_blank" className="w-fit">
            <Image
              src="/anima-logo.png"
              width={215}
              height={50}
              alt="Logo Anima"
              className="mb-0 md:mb-0 object-contain"
            />
          </Link>
          <p>{scopedT('anima_presentation')}</p>
          <Link href="https://animafrance.org/" target="_blank" className="fourth-button font-bold w-fit">
            {scopedT('anima_link')}
          </Link>
        </div>

        <div className="flex flex-col gap-5 max-w-[700px]">
          <Link href="https://animafrance.org/" target="_blank" className="w-fit">
            <figure className="flex flex-row justify-center align-center">
              <Image
              src="/dataforgood.svg"
              width={215}
              height={50}
              alt="Logo Data For Good"
              className="mb-0 md:mb-0 object-contain"
            />
            </figure>
          </Link>
          <p>{scopedT('dataforgood_presentation')}</p>
          <Link href="https://dataforgood.fr/" target="_blank" className="fourth-button font-bold w-fit">
            {scopedT('dataforgood_link')}
          </Link>
        </div>
      </div>
    </section>
  );
}
