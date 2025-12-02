import { getI18n } from '@/locales/server';
import StepColumnHeader from './step-column-header';
import BoltIconV2 from '../../ui/_components/BoltIconV2';
import SufferingSynthesisDurationRows from './suffering-scales';

interface SufferingSynthesisProps {
  title: string;
  percent: string;
  text: string;
  agony: string;
  pain: string;
  suffering: string;
  discomfort: string;
}

const SufferingSynthesis = ({ title, percent, text, agony, pain, suffering, discomfort }: SufferingSynthesisProps) => {
  return (
    <div className=" flex flex-col items-left gap-2 bg-grey rounded-[10px] p-[16px_20px_16px_20px]">
      <div className="flex items-center">
        <BoltIconV2 className="text-pink-3 h-[30px] min-w-[45px]" />
        <h5 className="text-center">{title}</h5>
      </div>

      <div className="flex gap-2 justify-center items-center">
        <p className="text-body font-bold w-1/2">
          {percent}
          {text}
        </p>

        <div className="w-full grid grid-cols-2 grid-rows-2 normal-case text-center">
          <SufferingSynthesisDurationRows
            agony_duration_text={agony}
            pain_duration_text={pain}
            suffering_duration_text={suffering}
            discomfort_duration_text={discomfort}
          />
        </div>
      </div>
    </div>
  );
};

export default async function StepThreeSufferingSummary() {
  const t = await getI18n();

  return (
    <article className="flex flex-col w-full md:w-[33%]">
      <StepColumnHeader title={t('MethodologyPage.sufferingQuantificationSteps.step3.title')} number="3" />
      <div className="flex flex-col gap-[10px] font-bold normal-case ">
        <SufferingSynthesis
          title={t('MethodologyPage.sufferingQuantificationSteps.step3.bloc1.title')}
          percent="33% "
          text={t('MethodologyPage.sufferingQuantificationSteps.step3.text1')}
          agony={t('MethodologyPage.sufferingQuantificationSteps.step3.bloc1.agony')}
          pain={t('MethodologyPage.sufferingQuantificationSteps.step3.bloc1.pain')}
          suffering={t('MethodologyPage.sufferingQuantificationSteps.step3.bloc1.suffering')}
          discomfort={t('MethodologyPage.sufferingQuantificationSteps.step3.bloc1.discomfort')}
        />

        <div className="bg-violet text-center text-h1 font-bold rounded-[10px] ">+</div>

        <SufferingSynthesis
          title={t('MethodologyPage.sufferingQuantificationSteps.step3.bloc2.title')}
          percent="100% "
          text={t('MethodologyPage.sufferingQuantificationSteps.step3.text1')}
          agony={t('MethodologyPage.sufferingQuantificationSteps.step3.bloc2.agony')}
          pain={t('MethodologyPage.sufferingQuantificationSteps.step3.bloc2.pain')}
          suffering={t('MethodologyPage.sufferingQuantificationSteps.step3.bloc2.suffering')}
          discomfort={t('MethodologyPage.sufferingQuantificationSteps.step3.bloc2.discomfort')}
        />

        <div className="bg-violet text-center text-h1 font-bold rounded-[10px]">+</div>

        <SufferingSynthesis
          title={t('MethodologyPage.sufferingQuantificationSteps.step3.bloc3.title')}
          percent="48% "
          text={t('MethodologyPage.sufferingQuantificationSteps.step3.text1')}
          agony={t('MethodologyPage.sufferingQuantificationSteps.step3.bloc3.agony')}
          pain={t('MethodologyPage.sufferingQuantificationSteps.step3.bloc3.pain')}
          suffering={t('MethodologyPage.sufferingQuantificationSteps.step3.bloc3.suffering')}
          discomfort={t('MethodologyPage.sufferingQuantificationSteps.step3.bloc3.discomfort')}
        />

        <div className="bg-violet text-center text-h1 font-bold rounded-[10px]">+</div>

        <div className="flex items-center bg-grey rounded-[10px] p-[16px_20px_16px_20px]">
          <p className="uppercase text-caption">{t('MethodologyPage.sufferingQuantificationSteps.step3.text2')}</p>
        </div>

        <div className="bg-violet text-center text-h1 font-bold rounded-[10px]">=</div>

        <div className="flex flex-col items-center gap-2 bg-grey rounded-[10px] p-[16px_20px_16px_20px]">
          <h5 className="text-xs font-extrabold mb-2">
            {t('MethodologyPage.sufferingQuantificationSteps.step3.bloc5.title')}
          </h5>

          <div className="normal-case w-full">
            <SufferingSynthesisDurationRows
              agony_duration_text={t('MethodologyPage.sufferingQuantificationSteps.step3.bloc5.agony')}
              pain_duration_text={t('MethodologyPage.sufferingQuantificationSteps.step3.bloc5.pain')}
              suffering_duration_text={t('MethodologyPage.sufferingQuantificationSteps.step3.bloc5.suffering')}
              discomfort_duration_text={t('MethodologyPage.sufferingQuantificationSteps.step3.bloc5.discomfort')}
            />
          </div>
        </div>
      </div>
    </article>
  );
}
