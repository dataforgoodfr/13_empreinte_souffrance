import { getScopedI18n } from '@/locales/server';
import Link from 'next/link';
import Image from 'next/image';

export default async function AssociationPresentationSection() {
  const scopedT = await getScopedI18n('aboutPage.association_presentation_section');

  return (
    <section className="p-section bg-white flex justify-center">
      <div className="max-w-contain">
        <h1 className="mb-8 md:max-w-2/3 text-black">{scopedT('two_hens_out_five_title').toUpperCase()}</h1>
        <div className="flex flex-row gap-[20px] justify-between">
          {/* Anima */}
          <div className="flex flex-col items-start gap-5 max-w-[650px]">
            <Link href="https://animafrance.org/" target="_blank" className="w-fit">
              <Image
                src="/anima-logo.svg"
                width={215}
                height={50}
                alt="Logo Anima"
                className="mb-0 md:mb-0 object-contain"
              />
            </Link>
            <p className="text-body">{scopedT('anima_presentation')}</p>
            <Link href="https://animafrance.org/" target="_blank" className="pink-button">
              {scopedT('anima_link')}
            </Link>
          </div>

          {/* Data4Good */}
          <div className="flex flex-col items-start gap-5 max-w-[650px]">
            <Link href="https://dataforgood.fr/" target="_blank" className="w-fit">
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
            <p className="text-body">{scopedT('dataforgood_presentation')}</p>
            <Link href="https://dataforgood.fr/" target="_blank" className="pink-button">
              {scopedT('dataforgood_link')}
            </Link>
          </div>
        </div>
      </div>
    </section>
  );
}
