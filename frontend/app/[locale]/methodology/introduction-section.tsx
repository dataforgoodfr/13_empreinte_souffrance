import { getI18n } from '@/locales/server';
import Link from 'next/link';

export default async function IntroductionSection() {
  const t = await getI18n();

  return (
    <section className="w-full bg-[#E7E4FF] py-8 md:py-16">
      <div className="w-full max-w-screen-xl mx-auto px-4 md:px-8">
        <img src="/welfare-footprint-logo.png " className="mb-10" alt="" />
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          {' '}
          <article>
            <p className="font-mono font-extrabold text-3xl">{t('MethodologyPage.introductionSection.title')}</p>
            <br />
            <p className="md:pr-20">{t('MethodologyPage.introductionSection.paragraph1')}</p>
            <br />
            <p className="md:pr-20">{t('MethodologyPage.introductionSection.paragraph2')}</p>
            <br />
            <p className="md:pr-20">{t('MethodologyPage.introductionSection.paragraph3')}</p>
          </article>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            <Scientist
              imgUrl={'/Cynthia-Schuck-Paim.png'}
              name={'Cynthia Schuck Paim'}
              text={t('MethodologyPage.introductionSection.scientist_text1')}
              link={'https://scholar.google.com/citations?user=9RGfMxMAAAAJ&hl=en&oi=ao'}
            />
            <Scientist
              imgUrl={'/Wladimir-J.Alonso.png'}
              name={'Wladimir J. Alonso'}
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
    <div className="text-center">
      <img src={imgUrl} alt="Scientist" className="w-55 rounded-full h-auto object-contain" />
      <p className="text-center font-bold my-5">{name}</p>
      <p className="text-justify text-sm text-gray-500">{text}</p>
      <Link className="font-light text-center" target="_blank" href={link}>
        ({t('MethodologyPage.introductionSection.list_here')})
      </Link>
    </div>
  );
};
