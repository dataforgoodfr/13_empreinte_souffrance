import { getI18n } from '@/locales/server';
import ContentWithImageSection from '@/app/[locale]/home/_components/content-with-image-component';
import Image from 'next/image';

export default async function ProgressSection() {
  const t = await getI18n();

  return (
    <section
      id="ProgressSection"
      className="min-h-screen py-8 w-full max-w-screen-xl mx-auto px-4 scroll-mt-18 flex flex-col justify-center items-center"
      aria-labelledby="results-heading"
    >
      <Image src="half-bars_egg.svg" width={150} height={250} alt={'TMP egg progress bars'} className="block p-2" />
      <h1
        id="results-heading"
        className="text-black flex flex-col text-center justify-center md:flex-row md:justify-start md:text-left items-center gap-8 mb-8"
      >
        {"title.toUpperCase()"}
      </h1>
      <div className="flex flex-col justify-center items-center">
        <div className="w-full md:5/6 lg:w-4/6 flex flex-col gap-7">
          <ContentWithImageSection
            text_heading={t('Results.agony.title')}
            text_content={t('Results.agony.content')}
            image_url="progress_bluegraph.png"
            image_description={t('Results.agony.image_description')}
            image_position="left"
          />
          <ContentWithImageSection
            text_heading={t('Results.discomfort.title')}
            text_content={t('Results.discomfort.content')}
            image_url="progress_redgraph.png"
            image_description={t('Results.discomfort.image_description')}
            image_position="right"
          />
          <ContentWithImageSection
            text_heading={t('Results.suffering_reduction.title')}
            text_content={t('Results.suffering_reduction.content')}
            image_url="progress_bakery.jpg"
            image_description={t('Results.suffering_reduction.image_description')}
            image_position="left"
          />
        </div>
      </div>
    </section>
  );
}
