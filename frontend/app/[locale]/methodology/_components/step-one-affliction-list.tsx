import { getI18n } from '@/locales/server';
import StepColumnHeader from './step-column-header';
import BoltIconV2 from '../../ui/_components/BoltIconV2';

async function StepOneAfflictionList() {
  const t = await getI18n();

  return (
    <article className=" flex flex-col w-full md:w-[33%] text-black">
      <StepColumnHeader title={t('MethodologyPage.sufferingQuantificationSteps.step1.title')} number="1" />
      <ul className="list-none flex flex-col gap-[10px] font-bold uppercase">
        <li className="flex space-between bg-grey rounded-[10px] items-center p-[16px_20px_16px_20px] ">
          <BoltIconV2 className="text-pink-3 h-[30px] mr-4" />
          <p className="text-h3 w-[52px] mr-4 font-bold">40%</p>
          <p className="text-caption">{t('MethodologyPage.sufferingQuantificationSteps.step1.text1')}</p>
        </li>
        <li className="flex space-between bg-grey rounded-[10px] items-center p-[16px_20px_16px_20px] ">
          <BoltIconV2 className="text-pink-3 h-[30px] mr-4" />
          <p className="text-h3 w-[52px] mr-4 font-bold">100%</p>
          <p className="text-caption">{t('MethodologyPage.sufferingQuantificationSteps.step1.text2')}</p>
        </li>
        <li className="flex space-between bg-grey rounded-[10px] items-center p-[16px_20px_16px_20px]">
          <BoltIconV2 className="text-pink-3 h-[30px] mr-4" />
          <p className="text-h3 w-[52px] mr-4 font-bold">5,5%</p>
          <p className="text-caption">{t('MethodologyPage.sufferingQuantificationSteps.step1.text3')}</p>
        </li>
        <li className="flex bg-grey rounded-[10px] items-center p-[16px_20px_16px_20px]">
          <p className="text-caption">{t('MethodologyPage.sufferingQuantificationSteps.step1.text4')}</p>
        </li>
      </ul>
    </article>
  );
}

export default StepOneAfflictionList;
