import { getI18n } from '@/locales/server';
import ListOfAffliction from './list-of-affition';

export default async function IdentifyPainSources() {
  const t = await getI18n();

  const listOfPain = [
    t('MethodologyPage.method_details_section.array_of_pain.pain_1'),
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
    t('MethodologyPage.method_details_section.array_of_pain.pain_15'),
    t('MethodologyPage.method_details_section.array_of_pain.pain_16'),
    t('MethodologyPage.method_details_section.array_of_pain.pain_17'),
    t('MethodologyPage.method_details_section.array_of_pain.pain_infected_skin_wound'),
    t('MethodologyPage.method_details_section.array_of_pain.pain_heat_stress'),
    t('MethodologyPage.method_details_section.array_of_pain.pain_dust_bath_deprivation'),
    t('MethodologyPage.method_details_section.array_of_pain.pain_infected_cloaca_wound'),
    t('MethodologyPage.method_details_section.array_of_pain.pain_fatal_cloaca_wound'),
  ];

  return (
    <div className="max-w-[935px] flex flex-col items-center gap-8">
      <hgroup className="max-w-[650px]">
        <h3 className="mb-4 uppercase ">{t('MethodologyPage.method_details_section.title')}</h3>
        <p className="mb-6">{t('MethodologyPage.method_details_section.description')}</p>
      </hgroup>

      {/* some psychologic pain */}
      <article className="w-full">
        <h4 className="">{t('MethodologyPage.method_details_section.section_img_1.title')}</h4>
        <hr className="border-1 border-pink-3 my-2" />
        <div className="flex flex-col md:flex-row m-auto gap-3 mt-4 ">
          <figure className="md:w-1/3 flex flex-col items-center gap-2">
            <img
              className="w-[330px] h-[220px] rounded-[10px] object-cover"
              src="/method-details/freedom-restriction.svg"
              alt={t('MethodologyPage.method_details_section.section_img_1.img_1.alt')}
            />
            <figcaption>
              <p className="mb-2 text-bold">
                {t('MethodologyPage.method_details_section.section_img_1.img_1.type_of_pain')}
              </p>
              <p> {t('MethodologyPage.method_details_section.section_img_1.img_1.description_of_pain')}</p>
            </figcaption>
          </figure>

          <figure className="md:w-1/3 flex flex-col items-center gap-2">
            <img
              className="w-[330px] h-[220px] rounded-[10px] object-cover"
              src="/method-details/nest-privation.svg"
              alt={t('MethodologyPage.method_details_section.section_img_1.img_2.alt')}
            />
            <figcaption>
              <p className="text-bold mb-2">
                {t('MethodologyPage.method_details_section.section_img_1.img_2.type_of_pain')}
              </p>
              <p> {t('MethodologyPage.method_details_section.section_img_1.img_2.description_of_pain')}</p>
            </figcaption>
          </figure>

          <figure className="md:w-1/3 flex flex-col items-center gap-2">
            <img
              className="w-[330px] h-[220px] rounded-[10px] object-cover"
              src="/method-details/behavior-privation.svg"
              alt={t('MethodologyPage.method_details_section.section_img_1.img_3.alt')}
            />
            <figcaption>
              <p className="text-bold mb-2">
                {t('MethodologyPage.method_details_section.section_img_1.img_3.type_of_pain')}
              </p>
              <p> {t('MethodologyPage.method_details_section.section_img_1.img_3.description_of_pain')}</p>
            </figcaption>
          </figure>
        </div>
      </article>

      {/* some physic pain */}
      <article className="w-full">
        <h4>{t('MethodologyPage.method_details_section.section_img_2.title')}</h4>
        <hr className="border-1 border-pink-3 my-2" />
        <div className="flex flex-col sm:flex-row m-auto gap-3 mt-4 ">
          <figure className="md:w-1/3 flex flex-col items-center gap-2">
            <img
              className="w-[330px] h-[220px] rounded-[10px] object-cover"
              src="/method-details/keelbone-fracture.svg"
              alt={t('MethodologyPage.method_details_section.section_img_2.img_1.alt')}
            />
            <figcaption>
              <p className="text-bold mb-2">
                {' '}
                {t('MethodologyPage.method_details_section.section_img_2.img_1.type_of_pain')}
              </p>
              <p> {t('MethodologyPage.method_details_section.section_img_2.img_1.description_of_pain')}</p>
            </figcaption>
          </figure>

          <figure className="md:w-1/3 flex flex-col items-center gap-2">
            <img
              className="w-[330px] h-[220px] rounded-[10px] object-cover"
              src="/method-details/peritonitis.svg"
              alt={t('MethodologyPage.method_details_section.section_img_2.img_2.alt')}
            />
            <figcaption>
              <p className="text-bold mb-2">
                {t('MethodologyPage.method_details_section.section_img_2.img_2.type_of_pain')}
              </p>
              <p> {t('MethodologyPage.method_details_section.section_img_2.img_2.description_of_pain')}</p>
            </figcaption>
          </figure>

          <figure className="md:w-1/3 flex flex-col items-center gap-2">
            <img
              className="w-[330px] h-[220px] rounded-[10px] object-cover"
              src="/method-details/lesions.svg"
              alt={t('MethodologyPage.method_details_section.section_img_2.img_3.alt')}
            />
            <figcaption>
              <p className="text-bold mb-2">
                {t('MethodologyPage.method_details_section.section_img_2.img_3.type_of_pain')}
              </p>
              <p> {t('MethodologyPage.method_details_section.section_img_2.img_3.description_of_pain')}</p>
            </figcaption>
          </figure>
        </div>
      </article>

      <article className="w-full">
        <h3 id="list_of_pains">{t('MethodologyPage.method_details_section.list_of_pains_h3')}</h3>
        <hr className="border-1 border-pink-3 my-2" />
        <ListOfAffliction
          listOfPain={listOfPain}
          seeMore={t('MethodologyPage.method_details_section.see_all_sources_btn')}
          seeLess={t('MethodologyPage.method_details_section.see_less_sources_btn')}
        />
      </article>
    </div>
  );
}
