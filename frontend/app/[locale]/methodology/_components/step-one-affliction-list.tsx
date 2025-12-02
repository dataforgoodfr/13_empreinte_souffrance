import { getI18n } from '@/locales/server';
import StepColumnHeader from './step-column-header';
import BoltIconV2 from '../../ui/_components/BoltIconV2';

async function StepOneAfflictionList() {
  const t = await getI18n();

  return (
    <article className=" flex flex-col w-full md:w-[33%] text-black">
      <StepColumnHeader title={t('MethodologyPage.sufferingQuantificationSteps.step1.title')} number="1" />
      <ul className="list-none flex flex-col gap-[10px] font-bold uppercase">
        <li className="flex bg-grey rounded-[10px] items-center p-[16px_20px_16px_20px] ">
          <BoltIconV2 className="text-pink-3 h-[30px] min-w-[45px]" />
          <p className="text-h2 min-w-[75px]">40%</p>
          <h5 className="text-caption">{t('MethodologyPage.sufferingQuantificationSteps.step1.text1')}</h5>
        </li>
        <li className="flex bg-grey rounded-[10px] items-center p-[16px_20px_16px_20px] ">
          <BoltIconV2 className="text-pink-3 h-[30px] min-w-[45px]" />
          <p className="text-h2 min-w-[75px]  ">100%</p>
          <h5 className="text-caption">{t('MethodologyPage.sufferingQuantificationSteps.step1.text2')}</h5>
        </li>
        <li className="flex bg-grey rounded-[10px] items-center p-[16px_20px_16px_20px]">
          <BoltIconV2 className="text-pink-3 h-[30px] min-w-[45px]" />
          <p className="text-h2 min-w-[75px]">5,5%</p>
          <h5 className="text-caption">{t('MethodologyPage.sufferingQuantificationSteps.step1.text3')}</h5>
        </li>
        <li className="flex bg-grey rounded-[10px] items-center p-[16px_20px_16px_20px]">
          <p className="text-caption">{t('MethodologyPage.sufferingQuantificationSteps.step1.text4')}</p>
        </li>
      </ul>
    </article>
  );
}

export default StepOneAfflictionList;
