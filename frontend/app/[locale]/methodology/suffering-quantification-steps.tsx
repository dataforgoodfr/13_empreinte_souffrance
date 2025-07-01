import { getI18n } from '@/locales/server';
import SectionHeading from '../ui/general/home-page/elements/section-heading';

/**
 * Quick documentation:
 * - SectionHeading: displays the section title.
 * - ChickenAfflictionsList: column 1, list of the hen's afflictions.
 * - AfflictionSufferingQuantifier: column 2, details and suffering tables.
 * - SufferingQuantificationTable: small table for each type of affliction.
 * - AverageSufferingSummary: column 3, visual summary of the total suffering.
 * - SynteseSurffering: synthesis block with a summary and a table.
 * - LegendPain: colored legend boxes to explain each methodological criterion.
 * - HeaderColone: stylized header for each column.
 */

export default async function SufferingQuantificationSteps() {
  const t = await getI18n();

  return (
    <section className="bg-white px-6 pb-20 py-2">
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
            titre={t('MethodologyPage.sufferingQuantificationSteps.legend.bloc1.title')}
            description={t('MethodologyPage.sufferingQuantificationSteps.legend.bloc1.description')}
            criteriaDesciption={t('MethodologyPage.sufferingQuantificationSteps.legend.bloc1.criteria_description')}
            criteria={t('MethodologyPage.sufferingQuantificationSteps.criteria')}
            color="#FFE9E9"
          />
          <LegendPain
            titre={t('MethodologyPage.sufferingQuantificationSteps.legend.bloc2.title')}
            description={t('MethodologyPage.sufferingQuantificationSteps.legend.bloc2.description')}
            criteriaDesciption={t('MethodologyPage.sufferingQuantificationSteps.legend.bloc2.criteria_description')}
            criteria={t('MethodologyPage.sufferingQuantificationSteps.criteria')}
            color="#FFC3C3"
          />
          <LegendPain
            titre={t('MethodologyPage.sufferingQuantificationSteps.legend.bloc3.title')}
            description={t('MethodologyPage.sufferingQuantificationSteps.legend.bloc3.description')}
            criteriaDesciption={t('MethodologyPage.sufferingQuantificationSteps.legend.bloc3.criteria_description')}
            criteria={t('MethodologyPage.sufferingQuantificationSteps.criteria')}
            color="#FF7B7B"
          />
          <LegendPain
            titre={t('MethodologyPage.sufferingQuantificationSteps.legend.bloc4.title')}
            description={t('MethodologyPage.sufferingQuantificationSteps.legend.bloc4.description')}
            criteriaDesciption={t('MethodologyPage.sufferingQuantificationSteps.legend.bloc4.criteria_description')}
            criteria={t('MethodologyPage.sufferingQuantificationSteps.criteria')}
            color="#3C1212"
            color_text="#FFFFFF"
          />
        </div>
      </div>
    </section>
  );
}

interface LegendProps {
  titre: string;
  description: string;
  criteriaDesciption: string;
  criteria: string;
  color: string;
  color_text?: string;
}

const LegendPain = ({ titre, description, criteriaDesciption, criteria, color, color_text }: LegendProps) => {
  return (
    <div className=" p-4  " style={{ backgroundColor: color, color: color_text }}>
      <h3 className="font-bold uppercase my-6">{titre}</h3>
      <p>{description}</p>
      <br />
      <span className="font-bold">{criteria} : </span>
      <span>{criteriaDesciption}</span>
    </div>
  );
};


type HeaderColoneProps = {
  title: string;
  number: number | string;
};

const HeaderColone = ({ title, number }: HeaderColoneProps) => {
  return (
    <div className="text-center font-extrabold font-mono bg-[#FF7B7B] py-3 px-2">
      <p className="text-5xl font-extrabold">{number}</p>
      <h2 className="">{title}</h2>
    </div>
  );
};


type StepProps = { t: ReturnType<typeof getI18n> extends Promise<infer R> ? R : never };

// column 1
const ChickenAfflictionsList = ({ t }: StepProps) => {
  return (
    <article className="border border-[#FF7B7B]  w-full md:basis-1/3 divide-y divide-[#FF7B7B]">
      <HeaderColone title={t('MethodologyPage.sufferingQuantificationSteps.step1.title')} number="1" />
      <ul className="list-none bg-white font-bold text-xs font-mono divide-y divide-[#FF7B7B] uppercase">
        <li className="flex items-center px-2 py-4 w-full gap-x-6">
          <p className="text-2xl font-bold w-15 flex-shrink-0 text-left">33%</p>
          <p className="flex-1 text-left">{t('MethodologyPage.sufferingQuantificationSteps.step1.text1')}</p>
        </li>
        <li className="flex items-center px-2 py-4 w-full gap-x-6">
          <p className="text-2xl font-bold w-15 flex-shrink-0 text-left">100%</p>
          <p className="flex-1 text-left">{t('MethodologyPage.sufferingQuantificationSteps.step1.text2')}</p>
        </li>
        <li className="flex items-center px-2 py-4 w-full gap-x-6">
          <p className="text-2xl font-bold w-15 flex-shrink-0 text-left">48%</p>
          <p className="flex-1 text-left">{t('MethodologyPage.sufferingQuantificationSteps.step1.text3')}</p>
        </li>
        <li className="flex items-center px-2 py-4 w-full gap-x-6">
          <p className="flex-1 text-left">{t('MethodologyPage.sufferingQuantificationSteps.step1.text4')}</p>
        </li>
      </ul>
    </article>
  );
};

// column 2
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
          <p className="p-1 w_80 text-center text-white bg-[#3C1212]">{agony}</p>
        </div>
        <div>
          <p className="p-1 w_80 text-center bg-[#FF7B7B]">{pain}</p>
        </div>
        <div>
          <p className="p-1 w_80 text-center bg-[#FFC3C3]">{suffering}</p>
        </div>
        <div>
          <p className="p-1 w_80 text-center bg-[#FFE9E9]">{discomfort}</p>
        </div>
      </div>
    </div>
  );
};

const AfflictionSufferingQuantifier = ({ t }: StepProps) => {
  return (
    <article className="border border-[#FF7B7B] divide-y divide-[#FF7B7B] md:basis-1/3  w-full ">
      <HeaderColone title={t('MethodologyPage.sufferingQuantificationSteps.step2.title')} number="2" />
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

// column 3
interface SynteseSurfferingProps {
  title: string;
  percent: string;
  text: string;
  agony: string;
  pain: string;
  suffering: string;
  discomfort: string;
}

const SynteseSurffering = ({ title, percent, text, agony, pain, suffering, discomfort }: SynteseSurfferingProps) => {
  return (
    <div className="bg-white p-3">
      <div className="flex items-center mb-2">
        <h3 className="font-bold uppercase text-sm">{title}</h3>
      </div>
      {/* Bas : contenu partagé gauche/droite */}
      <div className="flex justify-center text-xs ">
        {/* Moitié gauche : % + texte */}
        <div className="flex justify-center items-center normal-case gap-1 pr-2">
          <span className="font-bold">{percent}</span>
          <span className="font-bold">{text}</span>
        </div>
        {/* Moitié droite : grille */}
        <div className="flex items-center justify-end w-1/2">
          <div className="grid grid-cols-2 grid-rows-2 w-max text-[8px] text-left normal-case">
            <div className="bg-[#3C1212] text-white p-2">{agony}</div>
            <div className="bg-[#FF7B7B] text-[#3C1212] p-2">{pain}</div>
            <div className="bg-[#FFC3C3] text-[#3C1212] p-2">{suffering}</div>
            <div className="bg-[#FFE9E9] text-[#3C1212] p-2">{discomfort}</div>
          </div>
        </div>
      </div>
    </div>
  );
};

const AverageSufferingSummary = ({ t }: StepProps) => {
  return (
    <article className="flex-1 md:basis-1/3 divide-y divide-[#FF7B7B] border border-[#FF7B7B]">
      <HeaderColone title={t('MethodologyPage.sufferingQuantificationSteps.step3.title')} number="3" />
      <SynteseSurffering
        title={t('MethodologyPage.sufferingQuantificationSteps.step3.bloc1.title')}
        percent="33% "
        text={t('MethodologyPage.sufferingQuantificationSteps.step3.text1')}
        agony={t('MethodologyPage.sufferingQuantificationSteps.step3.bloc1.agony')}
        pain={t('MethodologyPage.sufferingQuantificationSteps.step3.bloc1.pain')}
        suffering={t('MethodologyPage.sufferingQuantificationSteps.step3.bloc1.suffering')}
        discomfort={t('MethodologyPage.sufferingQuantificationSteps.step3.bloc1.discomfort')}
      />
      <div className="bg-[#E7E4FF] text-center text-3xl font-extrabold">+</div>
      <SynteseSurffering
        title={t('MethodologyPage.sufferingQuantificationSteps.step3.bloc2.title')}
        percent="100% "
        text={t('MethodologyPage.sufferingQuantificationSteps.step3.text1')}
        agony={t('MethodologyPage.sufferingQuantificationSteps.step3.bloc2.agony')}
        pain={t('MethodologyPage.sufferingQuantificationSteps.step3.bloc2.pain')}
        suffering={t('MethodologyPage.sufferingQuantificationSteps.step3.bloc2.suffering')}
        discomfort={t('MethodologyPage.sufferingQuantificationSteps.step3.bloc2.discomfort')}
      />
      <div className="bg-[#E7E4FF] text-center text-3xl font-extrabold">+</div>
      <SynteseSurffering
        title={t('MethodologyPage.sufferingQuantificationSteps.step3.bloc3.title')}
        percent="48% "
        text={t('MethodologyPage.sufferingQuantificationSteps.step3.text1')}
        agony={t('MethodologyPage.sufferingQuantificationSteps.step3.bloc3.agony')}
        pain={t('MethodologyPage.sufferingQuantificationSteps.step3.bloc3.pain')}
        suffering={t('MethodologyPage.sufferingQuantificationSteps.step3.bloc3.suffering')}
        discomfort={t('MethodologyPage.sufferingQuantificationSteps.step3.bloc3.discomfort')}
      />
      <div className="bg-[#E7E4FF] text-center text-3xl font-extrabold">+</div>
      <div className="normal-case p-2 text-xs">{t('MethodologyPage.sufferingQuantificationSteps.step3.text2')}</div>
      <div className="bg-[#E7E4FF] text-center text-3xl font-extrabold">=</div>
      <div className="bg-white p-4">
        <h3 className="text-xs font-extrabold mb-2">
          {t('MethodologyPage.sufferingQuantificationSteps.step3.bloc5.title')}
        </h3>
        <div className="text-[9px] normal-case mx-auto">
          <div className="grid grid-cols-2 grid-rows-2 text-xs font-normal text-left normal-case mx-auto">
            <div className="bg-[#3C1212] text-white p-2">
              {t('MethodologyPage.sufferingQuantificationSteps.step3.bloc5.agony')}
            </div>
            <div className="bg-[#FF7B7B] text-[#3C1212] p-2">
              {t('MethodologyPage.sufferingQuantificationSteps.step3.bloc5.pain')}
            </div>
            <div className="bg-[#FFC3C3] text-[#3C1212] p-2">
              {t('MethodologyPage.sufferingQuantificationSteps.step3.bloc5.suffering')}
            </div>
            <div className="bg-[#FFE9E9] text-[#3C1212] p-2">
              {t('MethodologyPage.sufferingQuantificationSteps.step3.bloc5.discomfort')}
            </div>
          </div>
        </div>
      </div>
    </article>
  );
};
