import SectionHeading from '../ui/general/home-page/elements/section-heading';
import { getI18n } from '@/locales/server';

export default async function KeyResultsSection() {
  const t = await getI18n();

  return (
    <section className="bg-[#FFC3C3] px-6 pb-20 py-2">
      <div className="max-w-screen-xl mx-auto ">
        <SectionHeading title={t('MethodologyPage.key_results_section.key_results_h1')} heading_number="3" />
        <div className="md:w-1/2">
          <p>{t('MethodologyPage.key_results_section.text_1')}</p>
          <p className="py-2">{t('MethodologyPage.key_results_section.text_2')}</p>
        </div>
        <div className="grid md:grid-cols-2 grid-cols-1 gap-2 md:gap-1 mt-10">
          <CarteOfPain
            text={t('MethodologyPage.key_results_section.carte_1.text_carte_1')}
            agony={t('MethodologyPage.key_results_section.carte_1.agony_carte_1')}
            pain={t('MethodologyPage.key_results_section.carte_1.pain_carte_1')}
            suffering={t('MethodologyPage.key_results_section.carte_1.suffering_carte_1')}
            discomfort={t('MethodologyPage.key_results_section.carte_1.discomfort_carte_1')}
          />
          <CarteOfPain
            text={t('MethodologyPage.key_results_section.carte_2.text_carte_2')}
            agony={t('MethodologyPage.key_results_section.carte_2.agony_carte_2')}
            pain={t('MethodologyPage.key_results_section.carte_2.pain_carte_2')}
            suffering={t('MethodologyPage.key_results_section.carte_2.suffering_carte_2')}
            discomfort={t('MethodologyPage.key_results_section.carte_2.discomfort_carte_2')}
          />
          <CarteOfPain
            text={t('MethodologyPage.key_results_section.carte_3.text_carte_3')}
            agony={t('MethodologyPage.key_results_section.carte_3.agony_carte_3')}
            pain={t('MethodologyPage.key_results_section.carte_3.pain_carte_3')}
            suffering={t('MethodologyPage.key_results_section.carte_3.suffering_carte_3')}
            discomfort={t('MethodologyPage.key_results_section.carte_3.discomfort_carte_3')}
          />
          <CarteOfPain
            text={t('MethodologyPage.key_results_section.carte_4.text_carte_4')}
            agony={t('MethodologyPage.key_results_section.carte_4.agony_carte_4')}
            pain={t('MethodologyPage.key_results_section.carte_4.pain_carte_4')}
            suffering={t('MethodologyPage.key_results_section.carte_4.suffering_carte_4')}
            discomfort={t('MethodologyPage.key_results_section.carte_4.discomfort_carte_4')}
          />
        </div>
      </div>
    </section>
  );
}

interface CarteOfPainProps {
  text: string;
  agony: string;
  pain: string;
  suffering: string;
  discomfort: string;
}

const CarteOfPain = ({ text, agony, pain, suffering, discomfort }: CarteOfPainProps) => {
  return (
    <div className="bg-[#FFE9E9] flex  text-xs  border border-[#FF7B7B]">
      <div className="w-1/2 p-6 font-mono font-bold">
        <img src="/tmp_logo.webp" alt="" style={{ height: '50px', width: '50px' }} />
        <p>{text}</p>
      </div>
      <div className="w-1/2 flex flex-col items-center justify-center ">
        <p className="h-1/4 w-full text-center p-2 bg-[#3C1212] text-white">{agony}</p>
        <p className="h-1/4 w-full text-center p-2 bg-[#FF7B7B]">{pain}</p>
        <p className="h-1/4 w-full text-center p-2  bg-[#FFC3C3]">{suffering}</p>
        <p className="h-1/4 w-full text-center p-2  bg-[#FFE9E9]">{discomfort}</p>
      </div>
    </div>
  );
};
