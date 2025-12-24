import { getI18n } from '@/locales/server';
import PainTrackTable from './pain-track-table';

export default async function QuantifyPainBySources() {
  const t = await getI18n();

  return (
    <div className="w-full flex flex-col items-center gap-8">
      <hgroup className="max-w-[650px]">
        <h3 className="mb-4">{t('MethodologyPage.QuantifySufferingByPain.title')}</h3>
        <p className="text-md mb-6">{t('MethodologyPage.QuantifySufferingByPain.question')}</p>
        <p className="text-md mb-2">{t('MethodologyPage.QuantifySufferingByPain.description1')}</p>
        <p className="text-md mb-2">{t('MethodologyPage.QuantifySufferingByPain.description2')}</p>
        <p className="text-md mb-2">{t('MethodologyPage.QuantifySufferingByPain.description3')}</p>
      </hgroup>

      <div className="w-full">
        <h4 className="mb-4">{t('MethodologyPage.QuantifySufferingByPain.painTrackTableTitle')}</h4>
        <hr className="border-1 mb-10 border-pink-3" />
        <div className="bg-white rounded-[5px] mx-0 lg:mx-36">
          <PainTrackTable />
        </div>
      </div>
    </div>
  );
}
