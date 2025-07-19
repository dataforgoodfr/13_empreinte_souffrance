import { getI18n } from '@/locales/server';
import SectionHeading from '../ui/general/home-page/elements/section-heading';
import SufferingStagesDescription from "@/app/[locale]/ui/general/elements/suffering-stages-description";
import SufferingSynthesisDurationTable
  from "@/app/[locale]/ui/general/methodology/elements/suffering-synthesis-duration-table";
import SufferingSynthesisDurationRows
  from "@/app/[locale]/ui/general/methodology/elements/suffering-synthesis-duration-rows";

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

export default async function SufferingQuantificationSteps() {
  const t = await getI18n();

  return (
    <section className="bg-grey px-6 pb-20 py-2">
      <div className="max-w-screen-xl mx-auto ">
        <SectionHeading heading_number="1" title={t('MethodologyPage.sufferingQuantificationSteps.title')} />
        <div className="flex flex-col md:flex-row gap-2 items-start mx-auto max-w-screen-xl  md:py-8 uppercase w-full">
          <ChickenAfflictionsList />
          <AfflictionSufferingQuantifier />
          <AverageSufferingSummary />
        </div>

        <h2 className="text-3xl font-bold uppercase mt-6">
          {t('MethodologyPage.sufferingQuantificationSteps.title2')}
        </h2>
        <p className="md:max-w-2/3 my-6">{t('MethodologyPage.sufferingQuantificationSteps.text')}</p>
          <SufferingStagesDescription display_criteria={true}/>
      </div>
    </section>
  );
}

type StepColumnHeaderProps = {
  title: string;
  number: number | string;
};

const StepColumnHeader = ({ title, number }: StepColumnHeaderProps) => {
  return (
    <div className="text-center font-extrabold font-mono bg-pink-3 py-3 px-2">
      <p className="text-5xl font-extrabold">{number}</p>
      <h2 className="">{title}</h2>
    </div>
  );
};


async function ChickenAfflictionsList(){
    const t = await getI18n();

  return (
    <article className="border border-pink-3 w-full md:basis-1/3">
      <StepColumnHeader title={t('MethodologyPage.sufferingQuantificationSteps.step1.title')} number="1" />
      <ul className="list-none bg-white font-bold text-xs font-mono divide-y divide-pink-3 uppercase">
        <li className="flex items-center px-2 py-4 w-full gap-x-6">
          <p className="text-2xl font-bold w-15 flex-shrink-0 text-left">40%</p>
          <p className="flex-1 text-left">{t('MethodologyPage.sufferingQuantificationSteps.step1.text1')}</p>
        </li>
        <li className="flex items-center px-2 py-4 w-full gap-x-6">
          <p className="text-2xl font-bold w-15 flex-shrink-0 text-left">100%</p>
          <p className="flex-1 text-left">{t('MethodologyPage.sufferingQuantificationSteps.step1.text2')}</p>
        </li>
        <li className="flex items-center px-2 py-4 w-full gap-x-6">
          <p className="text-2xl font-bold w-15 flex-shrink-0 text-left">5,5%</p>
          <p className="flex-1 text-left">{t('MethodologyPage.sufferingQuantificationSteps.step1.text3')}</p>
        </li>
        <li className="flex items-center px-2 py-4 w-full gap-x-6">
          <p className="flex-1 text-left">{t('MethodologyPage.sufferingQuantificationSteps.step1.text4')}</p>
        </li>
      </ul>
    </article>
  );
};

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
    <div className="bg-white p-4">
      <h3 className="text-center font-bold mb-2">{title}</h3>
      <div className="normal-case">
        <SufferingSynthesisDurationRows agony_duration_text={agony} pain_duration_text={pain} suffering_duration_text={suffering} discomfort_duration_text={discomfort}/>
      </div>
    </div>
  );
};

async function AfflictionSufferingQuantifier() {
    const t = await getI18n();

    return (
    <article className="border border-pink-3 divide-y divide-pink-3 md:basis-1/3  w-full ">
      <StepColumnHeader title={t('MethodologyPage.sufferingQuantificationSteps.step2.title')} number="2" />
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
      <div className="flex items-center px-2 py-4 w-full gap-x-6">
        <p className="flex-1 text-left  font-bold text-xs font-mono">
          {t('MethodologyPage.sufferingQuantificationSteps.step1.text4')}
        </p>
      </div>
    </article>
  );
};

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
    <div className="bg-white p-3">
      <div className="flex items-center mb-2">
        <h3 className="font-bold uppercase text-sm">{title}</h3>
      </div>
      <div className="flex justify-center">
        <div className="flex justify-center items-center normal-case gap-1 pr-2">
          <span className="font-bold">{percent}</span>
          <span className="font-bold">{text}</span>
        </div>
        <div className="flex items-center justify-end w-1/2">
          <SufferingSynthesisDurationTable agony_duration_text={agony} pain_duration_text={pain} suffering_duration_text={suffering} discomfort_duration_text={discomfort}/>
        </div>
      </div>
    </div>
  );
};

async function AverageSufferingSummary() {
    const t = await getI18n();

    return (
    <article className="flex-1 md:basis-1/3 divide-y divide-pink-3 border border-pink-3">
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
      <div className="bg-violet-1 text-center text-3xl font-extrabold">+</div>
      <SufferingSynthesis
        title={t('MethodologyPage.sufferingQuantificationSteps.step3.bloc2.title')}
        percent="100% "
        text={t('MethodologyPage.sufferingQuantificationSteps.step3.text1')}
        agony={t('MethodologyPage.sufferingQuantificationSteps.step3.bloc2.agony')}
        pain={t('MethodologyPage.sufferingQuantificationSteps.step3.bloc2.pain')}
        suffering={t('MethodologyPage.sufferingQuantificationSteps.step3.bloc2.suffering')}
        discomfort={t('MethodologyPage.sufferingQuantificationSteps.step3.bloc2.discomfort')}
      />
      <div className="bg-violet-1 text-center text-3xl font-extrabold">+</div>
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
};
