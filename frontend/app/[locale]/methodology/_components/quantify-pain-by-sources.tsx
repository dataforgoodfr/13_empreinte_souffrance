import { getI18n } from '@/locales/server';
import Image from 'next/image';

export default async function QuantifyPainBySources() {
  const t = await getI18n();

  return (
    <div className="w-full flex flex-col items-center gap-8">
      <hgroup className="max-w-[650px]">
        <h2 className="mb-4">{t('MethodologyPage.QuantifySufferingByPain.title')}</h2>
        <p className="text-md mb-6">{t('MethodologyPage.QuantifySufferingByPain.question')}</p>
        <p className="text-md mb-2">{t('MethodologyPage.QuantifySufferingByPain.description1')}</p>
        <p className="text-md mb-2">{t('MethodologyPage.QuantifySufferingByPain.description2')}</p>
        <p className="text-md mb-2">{t('MethodologyPage.QuantifySufferingByPain.description3')}</p>
      </hgroup>

      <div className=" md:min-w-[950px]">
        <h3 className="mb-4">{t('MethodologyPage.QuantifySufferingByPain.painTrackTableTitle')}</h3>
        <hr className="border-1 mb-10 border-pink-3" />
        <div className="bg-white p-6 rounded-[5px]">
          {/* <PainTrackTable /> */}
          <Image
            src="/pain-track-table.png"
            width={640}
            height={840}
            alt={t('MethodologyPage.QuantifySufferingByPain.painTrackTableTitle')}
            className="w-full"
          />
        </div>
      </div>
    </div>
  );
}
