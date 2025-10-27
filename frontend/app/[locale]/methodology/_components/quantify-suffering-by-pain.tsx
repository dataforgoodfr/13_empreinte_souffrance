import { getI18n } from '@/locales/server';
import ButtonLink from '@/app/[locale]/ui/_components/button-link';
import PainTrackTable from './pain-track-table';

export default async function QuantifySufferingByPain() {
  const t = await getI18n();

  return (
    <div className="w-full max-w-screen-xl mx-auto mt-12 dark-text">
      <div className="flex flex-col p-6 sm:p-20 lg:p-0 md:w-2/3 m-auto">
        <h2 className="text-2xl font-extrabold mb-4 uppercase ">
          {t('MethodologyPage.QuantifySufferingByPain.title')}
        </h2>
        <p className="text-md mb-6">{t('MethodologyPage.QuantifySufferingByPain.question')}</p>
        <p className="text-md mb-2">{t('MethodologyPage.QuantifySufferingByPain.description1')}</p>
        <p className="text-md mb-2">{t('MethodologyPage.QuantifySufferingByPain.description2')}</p>
        <p className="text-md mb-2">{t('MethodologyPage.QuantifySufferingByPain.description3')}</p>
        <p className="text-md mb-2">{t('MethodologyPage.QuantifySufferingByPain.description4')}</p>
      </div>

      <div className="p-6  w-full lg:max-w-4xl lg:mx-auto">
        <h3 className="text-xl font-bold mb-4  uppercase">
          {t('MethodologyPage.QuantifySufferingByPain.painTrackTableTitle')}
        </h3>
        <hr className="border-1 mb-10 border-pink-3" />
        <div className="mb-12 overflow-x-auto w-full">
          <PainTrackTable />
        </div>
      </div>

      <div className="bg-white flex flex-col md:flex-row items-stretch w-full mb-12 ">
        <img
          src="/analyze-pain.png"
          className="w-full md:w-2/4 object-cover"
          alt={t('MethodologyPage.QuantifySufferingByPain.conclusionAltImg')}
          style={{ display: 'block' }}
        />
        <div className="flex flex-col gap-y-2 md:gap-y-10 justify-center md:w-2/4 px-6 md:px-12">
          <p className="text-md p-2 md:p-0 text-bold">{t('MethodologyPage.QuantifySufferingByPain.conclusionText')}</p>
          <div className="w-full flex justify-center pb-5">
            <ButtonLink
              href="#list_of_pains"
              aria_label={t('MethodologyPage.QuantifySufferingByPain.conclusionButton')}
              button_text={t('MethodologyPage.QuantifySufferingByPain.conclusionButton')}
              width="small"
            />
          </div>
        </div>
      </div>
    </div>
  );
}
