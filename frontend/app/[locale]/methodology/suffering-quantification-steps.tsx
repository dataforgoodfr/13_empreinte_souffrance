import { getI18n } from '@/locales/server';
import SectionHeading from '../ui/general/home-page/elements/section-heading';

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
          <ChickenAfflictionsList t={t} />
          <AfflictionSufferingQuantifier t={t} />
          <AverageSufferingSummary t={t} />
        </div>

        <h2 className="text-3xl font-bold uppercase mt-6">
          {t('MethodologyPage.sufferingQuantificationSteps.title2')}
        </h2>
        <p className="md:max-w-2/3 my-6">{t('MethodologyPage.sufferingQuantificationSteps.text')}</p>

        <div className="flex flex-col md:flex-row text-sm ">
          <LegendPain
            title={t('MethodologyPage.sufferingQuantificationSteps.legend.bloc1.title')}
            description={t('MethodologyPage.sufferingQuantificationSteps.legend.bloc1.description')}
            criteria_description={t('MethodologyPage.sufferingQuantificationSteps.legend.bloc1.criteria_description')}
            criteria={t('MethodologyPage.sufferingQuantificationSteps.criteria')}
            bg_color="pink-1"
          />
          <LegendPain
            title={t('MethodologyPage.sufferingQuantificationSteps.legend.bloc2.title')}
            description={t('MethodologyPage.sufferingQuantificationSteps.legend.bloc2.description')}
            criteria_description={t('MethodologyPage.sufferingQuantificationSteps.legend.bloc2.criteria_description')}
            criteria={t('MethodologyPage.sufferingQuantificationSteps.criteria')}
            bg_color="pink-2"
          />
          <LegendPain
            title={t('MethodologyPage.sufferingQuantificationSteps.legend.bloc3.title')}
            description={t('MethodologyPage.sufferingQuantificationSteps.legend.bloc3.description')}
            criteria_description={t('MethodologyPage.sufferingQuantificationSteps.legend.bloc3.criteria_description')}
            criteria={t('MethodologyPage.sufferingQuantificationSteps.criteria')}
            bg_color="pink-3"
          />
          <LegendPain
            title={t('MethodologyPage.sufferingQuantificationSteps.legend.bloc4.title')}
            description={t('MethodologyPage.sufferingQuantificationSteps.legend.bloc4.description')}
            criteria_description={t('MethodologyPage.sufferingQuantificationSteps.legend.bloc4.criteria_description')}
            criteria={t('MethodologyPage.sufferingQuantificationSteps.criteria')}
            bg_color="brown"
            text_color="light-text"
          />
        </div>
      </div>
    </section>
  );
}

interface LegendProps {
  title: string;
  description: string;
  criteria_description: string;
  criteria: string;
  bg_color: string;
  text_color?: string;
}

const LegendPain = ({ title, description, criteria_description, criteria, bg_color = 'pink-1', text_color = 'dark-text' }: LegendProps) => {


  return (
    <div className={`p-4 ${text_color} bg-${bg_color}`}>
      <h3 className="font-bold uppercase my-6">{title}</h3>
      <p>{description}</p>
      <br />
      <span className="font-bold">{criteria} : </span>
      <span>{criteria_description}</span>
    </div>
  );
};


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


type StepProps = { t: ReturnType<typeof getI18n> extends Promise<infer R> ? R : never };

const ChickenAfflictionsList = ({ t }: StepProps) => {
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
      <div className="text-xs normal-case">
        <div>
          <p className="p-1 w_80 text-center light-text bg-brown">{agony}</p>
        </div>
        <div>
          <p className="p-1 w_80 text-center bg-pink-3">{pain}</p>
        </div>
        <div>
          <p className="p-1 w_80 text-center bg-pink-2">{suffering}</p>
        </div>
        <div>
          <p className="p-1 w_80 text-center bg-pink-1">{discomfort}</p>
        </div>
      </div>
    </div>
  );
};

const AfflictionSufferingQuantifier = ({ t }: StepProps) => {
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
      <div className="flex justify-center text-xs ">
        <div className="flex justify-center items-center normal-case gap-1 pr-2">
          <span className="font-bold">{percent}</span>
          <span className="font-bold">{text}</span>
        </div>
        <div className="flex items-center justify-end w-1/2">
          <div className="grid grid-cols-2 grid-rows-2 w-max text-[8px] text-left normal-case">
            <div className="flex justify-center items-center bg-brown light-text p-2">{agony}</div>
            <div className="flex justify-center items-center bg-pink-3 dark-text p-2">{pain}</div>
            <div className="flex justify-center items-center bg-pink-2 dark-text p-2">{suffering}</div>
            <div className="flex justify-center items-center bg-pink-1 dark-text p-2">{discomfort}</div>
          </div>
        </div>
      </div>
    </div>
  );
};

const AverageSufferingSummary = ({ t }: StepProps) => {
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
        <div className="text-[9px] normal-case mx-auto">
          <div className="grid grid-cols-2 grid-rows-2 text-xs font-normal text-left normal-case mx-auto">
            <div className="flex justify-center items-center bg-brown light-text p-2">
              {t('MethodologyPage.sufferingQuantificationSteps.step3.bloc5.agony')}
            </div>
            <div className="flex justify-center items-center bg-pink-3 dark-text p-2">
              {t('MethodologyPage.sufferingQuantificationSteps.step3.bloc5.pain')}
            </div>
            <div className="flex justify-center items-center bg-pink-2 dark-text p-2">
              {t('MethodologyPage.sufferingQuantificationSteps.step3.bloc5.suffering')}
            </div>
            <div className="flex justify-center items-center bg-pink-1 dark-text p-2">
              {t('MethodologyPage.sufferingQuantificationSteps.step3.bloc5.discomfort')}
            </div>
          </div>
        </div>
      </div>
    </article>
  );
};
