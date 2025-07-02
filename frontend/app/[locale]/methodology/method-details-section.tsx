import { getI18n } from '@/locales/server';
import QuantifySufferingByPain from '@/app/[locale]/methodology/quantify-suffering-by-pain';
import GlobalSufferingFigure from './global-suffering-figure';
import SectionHeading from '../ui/general/home-page/elements/section-heading';
import ListOfPAffition from './list-of-affition';

export default async function MethodDetailsSection() {
  const t = await getI18n();

  const listOfPain = [
    t('MethodologyPage.method_details_section.array_of_pain.pain_1'),
    t('MethodologyPage.method_details_section.array_of_pain.pain_2'),
    t('MethodologyPage.method_details_section.array_of_pain.pain_3'),
    t('MethodologyPage.method_details_section.array_of_pain.pain_4'),
    t('MethodologyPage.method_details_section.array_of_pain.pain_5'),
    t('MethodologyPage.method_details_section.array_of_pain.pain_6'),
    t('MethodologyPage.method_details_section.array_of_pain.pain_7'),
    t('MethodologyPage.method_details_section.array_of_pain.pain_8'),
    t('MethodologyPage.method_details_section.array_of_pain.pain_9'),
    t('MethodologyPage.method_details_section.array_of_pain.pain_10'),
    t('MethodologyPage.method_details_section.array_of_pain.pain_11'),
    t('MethodologyPage.method_details_section.array_of_pain.pain_12'),
    t('MethodologyPage.method_details_section.array_of_pain.pain_13'),
    t('MethodologyPage.method_details_section.array_of_pain.pain_14'),
    t('MethodologyPage.method_details_section.array_of_pain.pain_15'),
    t('MethodologyPage.method_details_section.array_of_pain.pain_16'),
    t('MethodologyPage.method_details_section.array_of_pain.pain_17'),
  ];

  return (
    <>
      <div className="w-full max-w-screen-xl mx-auto mt-12 text-[#3C1212]">
        <SectionHeading title={t('MethodologyPage.method_details_section.title_h1')} heading_number="2" />
        <div className="flex flex-col p-6  sm:p-20 lg:p-0 md:w-2/3 m-auto">
          <h2 className="text-2xl font-extrabold mb-4 uppercase ">
            {t('MethodologyPage.method_details_section.title_h2')}
          </h2>
          <p className="text-md mb-6">{t('MethodologyPage.method_details_section.question')}</p>
          <p className="text-md mb-6">{t('MethodologyPage.method_details_section.description')}</p>
        </div>
        <div className=" mx-auto ">
          <article className="p-6">
            <h3 className="uppercase font-bold ">
              {t('MethodologyPage.method_details_section.section_img_1.title_h3')}
            </h3>
            <hr className="border-1  border-[#FF7B7B] my-2" />
            <div className="flex flex-col sm:flex-row m-auto gap-3 mt-4 ">
              <div className="sm:w-1/3 flex flex-col items-center">
                {/* todo! change img */}
                <img
                  className="w-[350px] h-[350px] object-cover"
                  src="/restriction_of_freedom_of_movement.png"
                  alt=" {t('MethodologyPage.method_details_section.section_img_1.img_1.alt')}"
                />
                <p className="font-bold mb-2">
                  {t('MethodologyPage.method_details_section.section_img_1.img_1.type_of_pain')}
                </p>
                <p> {t('MethodologyPage.method_details_section.section_img_1.img_1.description_of_pain')}</p>
              </div>
              <div className="sm:w-1/3 flex flex-col items-center">
                {/* todo! change img */}
                <img
                  className="w-[350px] h-[350px] object-cover"
                  src="/nid_privation.png"
                  alt=" {t('MethodologyPage.method_details_section.section_img_1.img_2.alt')}"
                />
                <p className="font-bold mb-2">
                  {t('MethodologyPage.method_details_section.section_img_1.img_2.type_of_pain')}
                </p>
                <p> {t('MethodologyPage.method_details_section.section_img_1.img_2.description_of_pain')}</p>
              </div>
              <div className="sm:w-1/3 flex flex-col items-center">
                {/* todo! change img */}
                <img
                  className="w-[350px] h-[350px] object-cover"
                  src="/behavioral_deprivation.png"
                  alt=" {t('MethodologyPage.method_details_section.section_img_1.img_3.alt')}"
                />
                <p className="font-bold mb-2">
                  {t('MethodologyPage.method_details_section.section_img_1.img_3.type_of_pain')}
                </p>
                <p> {t('MethodologyPage.method_details_section.section_img_1.img_3.description_of_pain')}</p>
              </div>
            </div>
          </article>
          <article className=" p-6">
            <h3 className="uppercase font-bold ">
              {t('MethodologyPage.method_details_section.section_img_2.title_h3')}
            </h3>
            <hr className="border-1  border-[#FF7B7B] my-2" />
            <div className="flex flex-col sm:flex-row m-auto gap-3 mt-4 ">
              <div className="sm:w-1/3 flex flex-col items-center">
                {/* todo! change img */}
                <img
                  className="w-[350px] h-[350px] object-cover"
                  src="/breastbone_fracture.png"
                  alt=" {t('MethodologyPage.method_details_section.section_img_2.img_1.alt')}"
                />
                <p className="font-bold mb-2">
                  {' '}
                  {t('MethodologyPage.method_details_section.section_img_2.img_1.type_of_pain')}
                </p>
                <p> {t('MethodologyPage.method_details_section.section_img_2.img_1.description_of_pain')}</p>
              </div>
              <div className="sm:w-1/3 flex flex-col items-center">
                {/* todo! change img */}
                <img
                  className="w-[350px] h-[350px] object-cover"
                  src="/peritonitis.png"
                  alt=" {t('MethodologyPage.method_details_section.section_img_2.img_2.alt')}"
                />
                <p className="font-bold mb-2">
                  {t('MethodologyPage.method_details_section.section_img_2.img_2.type_of_pain')}
                </p>
                <p> {t('MethodologyPage.method_details_section.section_img_2.img_2.description_of_pain')}</p>
              </div>
              <div className="sm:w-1/3 flex flex-col items-center">
                {/* todo!: change img */}
                <img
                  className="w-[350px] h-[350px] object-cover"
                  src="/tissue_damage.png"
                  alt=" {t('MethodologyPage.method_details_section.section_img_2.img_3.alt')}"
                />
                <p className="font-bold mb-2">
                  {t('MethodologyPage.method_details_section.section_img_2.img_3.type_of_pain')}
                </p>
                <p> {t('MethodologyPage.method_details_section.section_img_2.img_3.description_of_pain')}</p>
              </div>
            </div>
          </article>
          <article className=" p-6">
            <h3 id="list_of_pains" className="uppercase font-bold scroll-mt-22 md:scroll-mt-18">
              {t('MethodologyPage.method_details_section.list_of_pains_h3')}
            </h3>
            <hr className="border-1  border-[#FF7B7B] my-2" />
            <ListOfPAffition
              listOfPain={listOfPain}
              seeMore={t('MethodologyPage.method_details_section.see_all_sources_btn')}
              seeLess={t('MethodologyPage.method_details_section.see_less_sources_btn')}
            />
          </article>
        </div>
      </div>

      <QuantifySufferingByPain />
      <GlobalSufferingFigure />
    </>
  );
}
