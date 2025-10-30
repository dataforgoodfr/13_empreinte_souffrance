import { getI18n } from '@/locales/server';
import QuantifySufferingByPain from '../_components/quantify-suffering-by-pain';
import GlobalSufferingFigure from '../_components/global-suffering-figure';
import SectionHeading from '../../ui/_sections/section-heading';
import ListOfAffliction from '../_components/list-of-affition';
import IdentifyPainSources from '../_components/identify_pain_sources';

export default async function MethodDetailsSection() {
  const t = await getI18n();

  return (
    <section className="p-section bg-pink-1">
      <SectionHeading title={t('MethodologyPage.method_details_section.title_h1')} heading_number="2" />

      <div className="flex flex-col items-center mt-15">
        <IdentifyPainSources />
      </div>
    </section>

    // <div className="bg-pink-1">
    //   <div className="w-full max-w-screen-xl mx-auto mt-12 dark-text">
    //    
    //     <div className="flex flex-col p-6  sm:p-20 lg:p-0 md:w-2/3 m-auto">
    //       <h2 className="text-2xl font-extrabold mb-4 uppercase ">
    //         {t('MethodologyPage.method_details_section.title_h2')}
    //       </h2>
    //       <p className="text-md mb-6">{t('MethodologyPage.method_details_section.question')}</p>
    //       <p className="text-md mb-6">{t('MethodologyPage.method_details_section.description')}</p>
    //     </div>
    //     <div className=" mx-auto ">
    //       <article className="p-6">
    //         <h3 className="uppercase font-bold ">
    //           {t('MethodologyPage.method_details_section.section_img_1.title_h3')}
    //         </h3>
    //         <hr className="border-1  border-pink-3 my-2" />
    //         <div className="flex flex-col sm:flex-row m-auto gap-3 mt-4 ">
    //           <div className="sm:w-1/3 flex flex-col items-center">

    //             <img
    //               className="w-[350px] h-[350px] object-cover"
    //               src="/restriction_of_freedom_of_movement.png"
    //               alt=" {t('MethodologyPage.method_details_section.section_img_1.img_1.alt')}"
    //             />
    //             <p className="font-bold mb-2">
    //               {t('MethodologyPage.method_details_section.section_img_1.img_1.type_of_pain')}
    //             </p>
    //             <p> {t('MethodologyPage.method_details_section.section_img_1.img_1.description_of_pain')}</p>
    //           </div>
    //           <div className="sm:w-1/3 flex flex-col items-center">
    //             {/* todo! change img */}
    //             <img
    //               className="w-[350px] h-[350px] object-cover"
    //               src="/nid_privation.png"
    //               alt=" {t('MethodologyPage.method_details_section.section_img_1.img_2.alt')}"
    //             />
    //             <p className="font-bold mb-2">
    //               {t('MethodologyPage.method_details_section.section_img_1.img_2.type_of_pain')}
    //             </p>
    //             <p> {t('MethodologyPage.method_details_section.section_img_1.img_2.description_of_pain')}</p>
    //           </div>
    //           <div className="sm:w-1/3 flex flex-col items-center">
    //             {/* todo! change img */}
    //             <img
    //               className="w-[350px] h-[350px] object-cover"
    //               src="/behavioral_deprivation.png"
    //               alt=" {t('MethodologyPage.method_details_section.section_img_1.img_3.alt')}"
    //             />
    //             <p className="font-bold mb-2">
    //               {t('MethodologyPage.method_details_section.section_img_1.img_3.type_of_pain')}
    //             </p>
    //             <p> {t('MethodologyPage.method_details_section.section_img_1.img_3.description_of_pain')}</p>
    //           </div>
    //         </div>
    //       </article>
    //       <article className=" p-6">
    //         <h3 className="uppercase font-bold ">
    //           {t('MethodologyPage.method_details_section.section_img_2.title_h3')}
    //         </h3>
    //         <hr className="border-1  border-pink-3 my-2" />
    //         <div className="flex flex-col sm:flex-row m-auto gap-3 mt-4 ">
    //           <div className="sm:w-1/3 flex flex-col items-center">
    //             {/* todo! change img */}
    //             <img
    //               className="w-[350px] h-[350px] object-cover"
    //               src="/breastbone_fracture.png"
    //               alt=" {t('MethodologyPage.method_details_section.section_img_2.img_1.alt')}"
    //             />
    //             <p className="font-bold mb-2">
    //               {' '}
    //               {t('MethodologyPage.method_details_section.section_img_2.img_1.type_of_pain')}
    //             </p>
    //             <p> {t('MethodologyPage.method_details_section.section_img_2.img_1.description_of_pain')}</p>
    //           </div>
    //           <div className="sm:w-1/3 flex flex-col items-center">
    //             {/* todo! change img */}
    //             <img
    //               className="w-[350px] h-[350px] object-cover"
    //               src="/peritonitis.png"
    //               alt=" {t('MethodologyPage.method_details_section.section_img_2.img_2.alt')}"
    //             />
    //             <p className="font-bold mb-2">
    //               {t('MethodologyPage.method_details_section.section_img_2.img_2.type_of_pain')}
    //             </p>
    //             <p> {t('MethodologyPage.method_details_section.section_img_2.img_2.description_of_pain')}</p>
    //           </div>
    //           <div className="sm:w-1/3 flex flex-col items-center">
    //             {/* todo!: change img */}
    //             <img
    //               className="w-[350px] h-[350px] object-cover"
    //               src="/tissue_damage.png"
    //               alt=" {t('MethodologyPage.method_details_section.section_img_2.img_3.alt')}"
    //             />
    //             <p className="font-bold mb-2">
    //               {t('MethodologyPage.method_details_section.section_img_2.img_3.type_of_pain')}
    //             </p>
    //             <p> {t('MethodologyPage.method_details_section.section_img_2.img_3.description_of_pain')}</p>
    //           </div>
    //         </div>
    //       </article>
    //       <article className=" p-6">
    //         <h3 id="list_of_pains" className="uppercase font-bold scroll-mt-22 md:scroll-mt-18">
    //           {t('MethodologyPage.method_details_section.list_of_pains_h3')}
    //         </h3>
    //         <hr className="border-1  border-pink-3 my-2" />
    //         <ListOfAffliction
    //           listOfPain={listOfPain}
    //           seeMore={t('MethodologyPage.method_details_section.see_all_sources_btn')}
    //           seeLess={t('MethodologyPage.method_details_section.see_less_sources_btn')}
    //         />
    //       </article>
    //     </div>
    //   </div>

    //   <QuantifySufferingByPain />
    //   <GlobalSufferingFigure />
    // </div>
  );
}
