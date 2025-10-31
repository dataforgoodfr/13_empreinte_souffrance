import { getI18n } from '@/locales/server';
import StepColumnHeader from './step-column-header';

import BoltIconV2 from '../../ui/_components/BoltIconV2';
import SufferingScales from './suffering-scales';

//* Sub-Component_______________

interface SufferingQuantificationTableProps {
  title: string;
  agony: string;
  pain: string;
  suffering: string;
  discomfort: string;
}

const SufferingQuantificationTable = ({
  title,
  agony,
  pain,
  suffering,
  discomfort,
}: SufferingQuantificationTableProps) => {
  return (
    <div className="flex flex-col gap-2 items-center bg-grey rounded-[10px] p-[16px_20px_16px_20px]">
      <div className="flex gap-2 justify-between items-center ">
        <BoltIconV2 className="text-pink-3 h-[30px]" />
        <p className="text-caption text-center font-bold">{title}</p>
      </div>
      <div className="normal-case w-full">
        <SufferingScales
          agony_duration_text={agony}
          pain_duration_text={pain}
          suffering_duration_text={suffering}
          discomfort_duration_text={discomfort}
        />
      </div>
    </div>
  );
};
// *___________________

async function StepTwoSufferingQuantification() {
  const t = await getI18n();

  return (
    <article className="flex flex-col w-full md:w-[33%]">
      <StepColumnHeader title={t('MethodologyPage.sufferingQuantificationSteps.step2.title')} number="2" />
      <div className="flex flex-col gap-[10px] font-bold ">
        <SufferingQuantificationTable
          title={t('MethodologyPage.sufferingQuantificationSteps.step2.bloc1.text')}
          agony={t('MethodologyPage.sufferingQuantificationSteps.step2.bloc1.agony')}
          pain={t('MethodologyPage.sufferingQuantificationSteps.step2.bloc1.pain')}
          suffering={t('MethodologyPage.sufferingQuantificationSteps.step2.bloc1.suffering')}
          discomfort={t('MethodologyPage.sufferingQuantificationSteps.step2.bloc1.discomfort')}
        />
        <SufferingQuantificationTable
          title={t('MethodologyPage.sufferingQuantificationSteps.step2.bloc2.text')}
          agony={t('MethodologyPage.sufferingQuantificationSteps.step2.bloc1.agony')}
          pain={t('MethodologyPage.sufferingQuantificationSteps.step2.bloc1.pain')}
          suffering={t('MethodologyPage.sufferingQuantificationSteps.step2.bloc1.suffering')}
          discomfort={t('MethodologyPage.sufferingQuantificationSteps.step2.bloc1.discomfort')}
        />
        <SufferingQuantificationTable
          title={t('MethodologyPage.sufferingQuantificationSteps.step2.bloc3.text')}
          agony={t('MethodologyPage.sufferingQuantificationSteps.step2.bloc1.agony')}
          pain={t('MethodologyPage.sufferingQuantificationSteps.step2.bloc1.pain')}
          suffering={t('MethodologyPage.sufferingQuantificationSteps.step2.bloc1.suffering')}
          discomfort={t('MethodologyPage.sufferingQuantificationSteps.step2.bloc1.discomfort')}
        />
        <div className="flex items-center bg-grey rounded-[10px] p-[16px_20px_16px_20px]">
          <p className="text-caption">{t('MethodologyPage.sufferingQuantificationSteps.step1.text4')}</p>
        </div>
      </div>
    </article>
  );
}

export default StepTwoSufferingQuantification;
