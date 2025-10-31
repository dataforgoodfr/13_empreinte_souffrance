import { getI18n } from '@/locales/server';
import Link from 'next/link';
import ButtonLink from '@/app/[locale]/ui/_components/button-link';
import PainTrackTable from './pain-track-table';

export default async function QuantifyPainBySources() {
  const t = await getI18n();

  return (
    <div className="max-w-[935px] flex flex-col items-center gap-8">
      <hgroup className="max-w-[650px]">
        <h2 className="text-2xl font-extrabold mb-4 uppercase ">
          {t('MethodologyPage.QuantifySufferingByPain.title')}
        </h2>
        <p className="text-md mb-6">{t('MethodologyPage.QuantifySufferingByPain.question')}</p>
        <p className="text-md mb-2">{t('MethodologyPage.QuantifySufferingByPain.description1')}</p>
        <p className="text-md mb-2">{t('MethodologyPage.QuantifySufferingByPain.description2')}</p>
        <p className="text-md mb-2">{t('MethodologyPage.QuantifySufferingByPain.description3')}</p>
        <p className="text-md mb-2">{t('MethodologyPage.QuantifySufferingByPain.description4')}</p>
      </hgroup>

      <div className="p-6  w-full lg:max-w-4xl lg:mx-auto">
        <h3 className="text-xl font-bold mb-4  uppercase">
          {t('MethodologyPage.QuantifySufferingByPain.painTrackTableTitle')}
        </h3>
        <hr className="border-1 mb-10 border-pink-3" />
        <div className="bg-white p-6 rounded-[10px]">
          <PainTrackTable />
        </div>
      </div>

      <figure className="bg-white flex flex-col md:flex-row items-stretch w-full mb-12 ">
        <img
          src="/img_placeholder.png"
          className="w-full md:w-2/4 object-cover"
          alt={t('MethodologyPage.QuantifySufferingByPain.conclusionAltImg')}
        />
        <figcaption className="flex flex-col items-center justify-center gap-6 px-6 md:px-12  ">
          <p className="text-body text-bold">{t('MethodologyPage.QuantifySufferingByPain.conclusionText')}</p>
          <Link className="primary-button text-button w-full" href="#list_of_pains">{t('MethodologyPage.QuantifySufferingByPain.conclusionButton')}</Link>
        </figcaption>
      </figure>
    </div>
  );
}
