import { getI18n } from '@/locales/server';
import SectionHeading from '../../ui/_sections/section-heading';
import SufferingStagesDescription from '@/app/[locale]/ui/_components/suffering-stages-description';
import SufferingSynthesisDurationTable from '@/app/[locale]/methodology/_components/suffering-synthesis-duration-table';
import SufferingSynthesisDurationRows from '@/app/[locale]/methodology/_components/suffering-synthesis-duration-rows';
import BoltIcon from '../../ui/_components/BoltIcon';
import BoltIconV2 from '../../ui/_components/BoltIconV2';

/**
 * Quick documentation:
 * - SectionHeading: displays the section title.
 * - ChickenAfflictionsList: column 1, list of the hen's afflictions.
 * - AfflictionSufferingQuantifier: column 2, details and suffering tables.
 * - SufferingQuantificationTable: small table for each type of affliction.
 * - AverageSufferingSummary: column 3, visual summary of the total suffering.
 * - SufferingSynthesis: synthesis block with a summary and a table.
 * - LegendPain: colored legend boxes to explain each methodological criterion.
 * - HeaderColone: stylized header for each column.
 */

interface StepColumnHeaderProps {
  title: string;
  number: number | string;
}

interface SufferingQuantificationTableProps {
  title: string;
  agony: string;
  pain: string;
  suffering: string;
  discomfort: string;
}

interface SufferingSynthesisProps {
  title: string;
  percent: string;
  text: string;
  agony: string;
  pain: string;
  suffering: string;
  discomfort: string;
}

export default async function SufferingQuantificationStepsSection() {
  const t = await getI18n();

  return (
    <section className="p-section bg-white">
      <div className="">
        <SectionHeading heading_number="1" title={t('MethodologyPage.sufferingQuantificationSteps.title')} />
        <div className="flex flex-col md:flex-row gap-6 py-8 uppercase">
          <ChickenAfflictionsList />
          <AfflictionSufferingQuantifier />
          <AverageSufferingSummary />
        </div>
        <SufferingStagesDescription display_criteria={true} />
      </div>
    </section>
  );
}

// * Components *//

// Bloc titre
async function StepColumnHeader({ title, number }: StepColumnHeaderProps) {
  return (
    <div className="text-center rounded-[10px] mb-[10px] font-extrabold font-mono bg-pink-2 py-3 px-2">
      <h2 className="font-extrabold">{number}</h2>
      <h4 className="">{title}</h4>
    </div>
  );
}

// Liste N°1
async function ChickenAfflictionsList() {
  const t = await getI18n();

  return (
    <article className=" flex flex-col w-full md:w-[33%] text-black">
      <StepColumnHeader title={t('MethodologyPage.sufferingQuantificationSteps.step1.title')} number="1" />
      <ul className="list-none flex flex-col gap-[10px] font-bold uppercase">
        <li className="flex space-between bg-grey-2 rounded-[10px] items-center p-[16px_20px_16px_20px] ">
          <BoltIconV2 className="text-pink-3 h-[30px] mr-4" />
          <p className="text-h3 w-[52px] mr-4 font-bold">40%</p>
          <p className="text-caption">{t('MethodologyPage.sufferingQuantificationSteps.step1.text1')}</p>
        </li>
        <li className="flex space-between bg-grey-2 rounded-[10px] items-center p-[16px_20px_16px_20px] ">
          <BoltIconV2 className="text-pink-3 h-[30px] mr-4" />
          <p className="text-h3 w-[52px] mr-4 font-bold">100%</p>
          <p className="text-caption">{t('MethodologyPage.sufferingQuantificationSteps.step1.text2')}</p>
        </li>
        <li className="flex space-between bg-grey-2 rounded-[10px] items-center p-[16px_20px_16px_20px]">
          <BoltIconV2 className="text-pink-3 h-[30px] mr-4" />
          <p className="text-h3 w-[52px] mr-4 font-bold">5,5%</p>
          <p className="text-caption">{t('MethodologyPage.sufferingQuantificationSteps.step1.text3')}</p>
        </li>
        <li className="flex bg-grey-2 rounded-[10px] items-center p-[16px_20px_16px_20px]">
          <p className="text-caption">{t('MethodologyPage.sufferingQuantificationSteps.step1.text4')}</p>
        </li>
      </ul>
    </article>
  );
}

//
const SufferingQuantificationTable = ({
  title,
  agony,
  pain,
  suffering,
  discomfort,
}: SufferingQuantificationTableProps) => {
  return (
    <div className="flex flex-col gap-2 items-center bg-grey-2 rounded-[10px] p-[16px_20px_16px_20px]">
      <div className="flex gap-2 justify-between items-center ">
        <BoltIconV2 className="text-pink-3 h-[30px]" />
        <p className="text-caption text-center font-bold">{title}</p>
      </div>
      <div className="normal-case w-full">
        <SufferingSynthesisDurationRows
          agony_duration_text={agony}
          pain_duration_text={pain}
          suffering_duration_text={suffering}
          discomfort_duration_text={discomfort}
        />
      </div>
    </div>
  );
};

// Liste N°2
async function AfflictionSufferingQuantifier() {
  const t = await getI18n();

  return (
    <article className="flex flex-col w-full md:w-[33%]">
      <StepColumnHeader title={t('MethodologyPage.sufferingQuantificationSteps.step2.title')} number="2" />
      <div className="flex flex-col gap-[10px] font-bold uppercase">
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
        <div className="flex items-center bg-grey-2 rounded-[10px] p-[16px_20px_16px_20px]">
          <p className="text-caption">{t('MethodologyPage.sufferingQuantificationSteps.step1.text4')}</p>
        </div>
      </div>
    </article>
  );
}

// Liste N°3
const SufferingSynthesis = ({ title, percent, text, agony, pain, suffering, discomfort }: SufferingSynthesisProps) => {
  return (
    <div className=" flex flex-col items-center gap-2 bg-grey-2 rounded-[10px] p-[16px_20px_16px_20px]">
      <p className="font-bold uppercase text-caption">{title}</p>

      <div className="flex gap-2 justify-center items-center">
        <BoltIconV2 className="text-pink-3 h-[30px]" />
        <p className="text-caption font-bold w-1/2">
          {percent}
          {text}
        </p>

        <div className="flex items-center justify-end w-1/2">
          <SufferingSynthesisDurationTable
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

async function AverageSufferingSummary() {
  const t = await getI18n();

  return (
    <article className="flex-1 md:basis-1/3">
      <StepColumnHeader title={t('MethodologyPage.sufferingQuantificationSteps.step3.title')} number="3" />
      <SufferingSynthesis
        title={t('MethodologyPage.sufferingQuantificationSteps.step3.bloc1.title')}
        percent="33% "
        text={t('MethodologyPage.sufferingQuantificationSteps.step3.text1')}
        agony={t('MethodologyPage.sufferingQuantificationSteps.step3.bloc1.agony')}
        pain={t('MethodologyPage.sufferingQuantificationSteps.step3.bloc1.pain')}
        suffering={t('MethodologyPage.sufferingQuantificationSteps.step3.bloc1.suffering')}
        discomfort={t('MethodologyPage.sufferingQuantificationSteps.step3.bloc1.discomfort')}
      />
      <div className="bg-violet text-center text-3xl font-extrabold">+</div>
      <SufferingSynthesis
        title={t('MethodologyPage.sufferingQuantificationSteps.step3.bloc2.title')}
        percent="100% "
        text={t('MethodologyPage.sufferingQuantificationSteps.step3.text1')}
        agony={t('MethodologyPage.sufferingQuantificationSteps.step3.bloc2.agony')}
        pain={t('MethodologyPage.sufferingQuantificationSteps.step3.bloc2.pain')}
        suffering={t('MethodologyPage.sufferingQuantificationSteps.step3.bloc2.suffering')}
        discomfort={t('MethodologyPage.sufferingQuantificationSteps.step3.bloc2.discomfort')}
      />
      <div className="bg-violet text-center text-3xl font-extrabold">+</div>
      <SufferingSynthesis
        title={t('MethodologyPage.sufferingQuantificationSteps.step3.bloc3.title')}
        percent="48% "
        text={t('MethodologyPage.sufferingQuantificationSteps.step3.text1')}
        agony={t('MethodologyPage.sufferingQuantificationSteps.step3.bloc3.agony')}
        pain={t('MethodologyPage.sufferingQuantificationSteps.step3.bloc3.pain')}
        suffering={t('MethodologyPage.sufferingQuantificationSteps.step3.bloc3.suffering')}
        discomfort={t('MethodologyPage.sufferingQuantificationSteps.step3.bloc3.discomfort')}
      />
      <div className="bg-violet-1 text-center text-3xl font-extrabold">+</div>
      <div className="normal-case p-2 text-xs">{t('MethodologyPage.sufferingQuantificationSteps.step3.text2')}</div>
      <div className="bg-violet-1 text-center text-3xl font-extrabold">=</div>
      <div className="bg-white p-4">
        <h3 className="text-xs font-extrabold mb-2">
          {t('MethodologyPage.sufferingQuantificationSteps.step3.bloc5.title')}
        </h3>
        <div className="normal-case mx-auto">
          <SufferingSynthesisDurationTable
            agony_duration_text={t('MethodologyPage.sufferingQuantificationSteps.step3.bloc5.agony')}
            pain_duration_text={t('MethodologyPage.sufferingQuantificationSteps.step3.bloc5.pain')}
            suffering_duration_text={t('MethodologyPage.sufferingQuantificationSteps.step3.bloc5.suffering')}
            discomfort_duration_text={t('MethodologyPage.sufferingQuantificationSteps.step3.bloc5.discomfort')}
          />
        </div>
      </div>
    </article>
  );
}
