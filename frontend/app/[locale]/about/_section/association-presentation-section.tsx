import { getScopedI18n } from '@/locales/server';
import Link from 'next/link';

export default async function AssociationPresentationSection() {
  const scopedT = await getScopedI18n('aboutPage.association_presentation_section');

  return (
    <section className="section-padding bg-white">
      <h1 className="p-8 lg:max-w-[1150px] leading-[57px]">
        {scopedT('two_hens_out_five_title').toUpperCase()}
      </h1>
      <div className="flex flex-wrap lg:p-8 gap-8 justify-between">
        <div className="flex flex-col gap-5 max-w-[700px]">
          <Link href="https://animafrance.org/" target="_blank" className="w-fit">
            <img src="/anima-logo.png" alt="Logo Anima" className="h-[50px] object-contain " />
          </Link>
          <p>{scopedT('anima_presentation')}</p>
          <Link href="https://animafrance.org/" target="_blank" className="w-fit underline">
            {scopedT('anima_link')}
          </Link>
        </div>

        <div className="flex flex-col gap-5 max-w-[700px]">
          <Link href="https://animafrance.org/" target="_blank" className="w-fit">
            <figure className="flex flex-row justify-center align-center">
              <img src="/logo_data_for_good.png" alt="Logo Data For Good" className="h-[50px] object-contain" />
              <h4 className="flex items-center font-semibold m-0 pl-2">Data For Good</h4>
            </figure>
          </Link>
          <p>{scopedT('dataforgood_presentation')}</p>
          <Link
            href="https://dataforgood.fr/"
            target="_blank"
            className="underline inline-flex items-center gap-2 w-fit"
          >
            {scopedT('dataforgood_link')}
          </Link>
        </div>
      </div>
    </section>
  );
}
