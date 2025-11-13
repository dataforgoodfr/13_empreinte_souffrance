import { getI18n } from '@/locales/server';
import ListOfAffliction from './list-of-affition';

export default async function IdentifyPainSources() {
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
    <div className="max-w-[935px] flex flex-col items-center gap-8">
      <hgroup className="max-w-[650px]">
        <h2 className="mb-4 uppercase ">{t('MethodologyPage.method_details_section.title_h2')}</h2>
        <p className="mb-6">{t('MethodologyPage.method_details_section.question')}</p>
        <p className="mb-6">{t('MethodologyPage.method_details_section.description')}</p>
      </hgroup>

      {/* some psychologic pain */}
      <article className="w-full">
        <h3 className="uppercase font-bold ">{t('MethodologyPage.method_details_section.section_img_1.title_h3')}</h3>
        <hr className="border-1  border-pink-3 my-2" />
        <div className="flex flex-col md:flex-row m-auto gap-3 mt-4 ">
          <figure className="md:w-1/3 flex flex-col items-center gap-2">
            <img
              className="w-[310px] h-[220px] rounded-[10px] object-cover"
              src="/img_placeholder.png"
              alt=" {t('MethodologyPage.method_details_section.section_img_1.img_1.alt')}"
            />
            <figcaption>
              <p className="font-bold mb-2">
                {t('MethodologyPage.method_details_section.section_img_1.img_1.type_of_pain')}
              </p>
              <p> {t('MethodologyPage.method_details_section.section_img_1.img_1.description_of_pain')}</p>
            </figcaption>
          </figure>

          <figure className="md:w-1/3 flex flex-col items-center gap-2">
            <img
              className="w-[310px] h-[220px] rounded-[10px] object-cover"
              src="/img_placeholder.png"
              alt=" {t('MethodologyPage.method_details_section.section_img_1.img_2.alt')}"
            />
            <figcaption>
              <p className="font-bold mb-2">
                {t('MethodologyPage.method_details_section.section_img_1.img_2.type_of_pain')}
              </p>
              <p> {t('MethodologyPage.method_details_section.section_img_1.img_2.description_of_pain')}</p>
            </figcaption>
          </figure>

          <figure className="md:w-1/3 flex flex-col items-center gap-2">
            <img
              className="w-[310px] h-[220px] rounded-[10px] object-cover"
              src="/img_placeholder.png"
              alt=" {t('MethodologyPage.method_details_section.section_img_1.img_3.alt')}"
            />
            <figcaption>
              <p className="font-bold mb-2">
                {t('MethodologyPage.method_details_section.section_img_1.img_3.type_of_pain')}
              </p>
              <p> {t('MethodologyPage.method_details_section.section_img_1.img_3.description_of_pain')}</p>
            </figcaption>
          </figure>
        </div>
      </article>

      {/* some physic pain */}
      <article className="w-full">
        <h3 className="uppercase font-bold ">{t('MethodologyPage.method_details_section.section_img_2.title_h3')}</h3>
        <hr className="border-1 border-pink-3 my-2" />
        <div className="flex flex-col sm:flex-row m-auto gap-3 mt-4 ">
          <figure className="md:w-1/3 flex flex-col items-center gap-2">
            <img
              className="w-[310px] h-[220px] rounded-[10px] object-cover"
              src="/img_placeholder.png"
              alt=" {t('MethodologyPage.method_details_section.section_img_2.img_1.alt')}"
            />
            <figcaption>
              <p className="font-bold mb-2">
                {' '}
                {t('MethodologyPage.method_details_section.section_img_2.img_1.type_of_pain')}
              </p>
              <p> {t('MethodologyPage.method_details_section.section_img_2.img_1.description_of_pain')}</p>
            </figcaption>
          </figure>

          <figure className="md:w-1/3 flex flex-col items-center gap-2">
            <img
              className="w-[310px] h-[220px] rounded-[10px] object-cover"
              src="/img_placeholder.png"
              alt=" {t('MethodologyPage.method_details_section.section_img_2.img_2.alt')}"
            />
            <figcaption>
              <p className="font-bold mb-2">
                {t('MethodologyPage.method_details_section.section_img_2.img_2.type_of_pain')}
              </p>
              <p> {t('MethodologyPage.method_details_section.section_img_2.img_2.description_of_pain')}</p>
            </figcaption>
          </figure>

          <figure className="md:w-1/3 flex flex-col items-center gap-2">
            <img
              className="w-[310px] h-[220px] rounded-[10px] object-cover"
              src="/img_placeholder.png"
              alt=" {t('MethodologyPage.method_details_section.section_img_2.img_3.alt')}"
            />
            <figcaption>
              <p className="font-bold mb-2">
                {t('MethodologyPage.method_details_section.section_img_2.img_3.type_of_pain')}
              </p>
              <p> {t('MethodologyPage.method_details_section.section_img_2.img_3.description_of_pain')}</p>
            </figcaption>
          </figure>
        </div>
      </article>

      <article className="w-full">
        <h3 id="list_of_pains" className="uppercase font-bold">
          {t('MethodologyPage.method_details_section.list_of_pains_h3')}
        </h3>
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
