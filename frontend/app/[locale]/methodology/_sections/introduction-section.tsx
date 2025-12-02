import { getI18n } from '@/locales/server';
import Link from 'next/link';

export default async function IntroductionSection() {
  const t = await getI18n();

  return (
    <section className="bg-violet p-section flex justify-center ">
      <div className="max-w-contain  ">
        <img src="/welfare-footprint-logo.png " className="w-[300px] lg:w-[450px]" alt="" />
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 ">
          <article className='flex flex-col'>
            <h1>{t('MethodologyPage.introductionSection.title')}</h1>
            <br />
            <p>{t('MethodologyPage.introductionSection.paragraph1')}</p>
            <br />
            <p>{t('MethodologyPage.introductionSection.paragraph2')}</p>
            <br />
            <p>{t('MethodologyPage.introductionSection.paragraph3')}</p>
            <Link href="www.welfarefootprint.org" className="CTA white-button w-fit">
              www.welfarefootprint.org
            </Link>
          </article>
          <div className=" grid grid-cols-1 md:grid-cols-2 gap-8">
            <Scientist
              imgUrl={'/Cynthia-Schuck-Paim.png'}
              name={'Cynthia Schuck-Paim'}
              text={t('MethodologyPage.introductionSection.scientist_text1')}
              link={'https://scholar.google.com/citations?user=9RGfMxMAAAAJ&hl=en&oi=ao'}
            />
            <Scientist
              imgUrl={'/Wladimir-J.Alonso.png'}
              name={'Wladimir Jimenez Alonso'}
              text={t('MethodologyPage.introductionSection.scientist_text2')}
              link={'https://scholar.google.com/citations?user=9RGfMxMAAAAJ&hl=en&oi=ao'}
            />
          </div>
        </div>
      </div>
    </section>
  );
}

interface ScientistProps {
  imgUrl: string;
  name: string;
  text: string;
  link: string;
}

const Scientist = async ({ imgUrl, name, text, link }: ScientistProps) => {
  const t = await getI18n();
  return (
    <div className="text-center flex flex-col items-center">
      <img src={imgUrl} alt="Scientist" className="w-55 rounded-full h-auto object-contain" />
      <h2 className="text-center my-5">{name}</h2>
      <p className="caption text-justify">{text}</p>
    </div>
  );
};
