import { getI18n } from '@/locales/server';
import Link from 'next/link';

export default async function IntroductionSection() {
  const t = await getI18n();

  return (
    <section className="bg-violet p-section flex justify-center ">
      <div className="max-w-contain ">
        <img src="/welfare-footprint-logo.svg " className="w-[300px] lg:w-[450px]" alt="" />
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 ">
          <article className="flex flex-col">
            <h1>{t('MethodologyPage.introductionSection.title')}</h1>
            <br />
            <p>{t('MethodologyPage.introductionSection.paragraph1')}</p>
            <br />
            <p>{t('MethodologyPage.introductionSection.paragraph2')}</p>
            <br />
            <p>{t('MethodologyPage.introductionSection.paragraph3')}</p>
            <Link
              href="https://welfarefootprint.org/"
              target="_blank"
              rel="noopener noreferrer"
              className="CTA white-button w-fit"
            >
              welfarefootprint.org
            </Link>
          </article>
          <div className=" grid grid-cols-1 md:grid-cols-2 gap-8">
            <Scientist
              imgUrl={'/Cynthia-Schuck-Paim.png'}
              name={'Cynthia Schuck-Paim'}
              text={t('MethodologyPage.introductionSection.scientist_text1')}
            />
            <Scientist
              imgUrl={'/Wladimir-J.Alonso.png'}
              name={'Wladimir J. Alonso'}
              text={t('MethodologyPage.introductionSection.scientist_text2')}
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
}

const Scientist = async ({ imgUrl, name, text }: ScientistProps) => {
  return (
    <div className="text-center flex flex-col items-center">
      <img src={imgUrl} alt="Scientist" className="w-55 rounded-full h-auto object-contain" />
      <h2 className="text-center my-5">{name}</h2>
      <p className="caption text-justify">{text}</p>
    </div>
  );
};
