import { getI18n } from '@/locales/server';
import ArrowDown from '@/app/[locale]/ui/_logo/ArrowDown';
import type { StaticImageData } from 'next/image';
import Image from 'next/image';
import { ReactNode } from 'react';
import InfoContent from '@/app/[locale]/home/_components/InfoContent';
import Link from 'next/link';
import SectionTitle from '../_components/section-title';

export default async function ResultsSection() {
  const t = await getI18n();

  return (
    <section
      id="ResultSection"
      className="bg-violet min-h-screen py-8 scroll-mt-18 font-albert-sans"
      aria-labelledby="results-heading"
    >
      <div className="flex flex-col items-center">
        <SectionTitle
          image_path="full-bars_egg.svg"
          image_alt="egg shaped logo with a hen behind bars"
          title={<>{t('Results.title')}</>}
        />
        <p className="m-5 text-[1.1rem] font-bold max-w-4xl text-center mx-16">{t('Results.subtitle')}</p>
        <Link href={'#results-table'}>
          <ArrowDown className="mt-10" />
        </Link>
      </div>
      <div className="flex flex-col items-center gap-4 mt-15 mx-10" id={'results-table'}>
        {(
          [
            {
              infoContent: (
                <InfoContent
                  superTitle={t('Results.sectionList.first.superTitle')}
                  title={t('Results.sectionList.first.title')}
                  source={{
                    url: t('Results.sectionList.first.source.url'),
                    name: t('Results.sectionList.first.source.name'),
                  }}
                >
                  {t('Results.sectionList.first.text')}
                </InfoContent>
              ),
            },
            {
              infoContent: (
                <InfoContent
                  superTitle={t('Results.sectionList.second.superTitle')}
                  title={t('Results.sectionList.second.title')}
                  source={{
                    url: t('Results.sectionList.second.source.url'),
                    name: t('Results.sectionList.second.source.name'),
                  }}
                >
                  {t('Results.sectionList.second.text')}
                </InfoContent>
              ),
            },
            {
              infoContent: (
                <InfoContent
                  superTitle={t('Results.sectionList.third.superTitle')}
                  title={t('Results.sectionList.third.title')}
                  source={{
                    url: t('Results.sectionList.third.source.url'),
                    name: t('Results.sectionList.third.source.name'),
                  }}
                >
                  {t('Results.sectionList.third.text')}
                </InfoContent>
              ),
            },
          ] as {
            infoContent: ReactNode;
            imageSrc?: string | StaticImageData;
          }[]
        ).map(({ infoContent, imageSrc }, index) => (
          <div
            className={`inline-flex /
              ${index % 2 ? 'lg:flex-row-reverse' : 'lg:flex-row'} /
              flex-col rounded-md overflow-hidden /
              bg-white max-w-screen-xl
              h-[840px] lg:h-[420px]
              w-[420px] lg:w-full
              `}
            key={index}
          >
            <div className="w-full lg:w-1/2 h-2/3 lg:h-full p-5 flex-shrink-0">{infoContent}</div>
            <div className="w-full lg:w-1/2 h-1/3 lg:h-full flex-shrink-0">
              <Image
                width={500}
                height={500}
                className="w-full h-full object-cover"
                src={imageSrc ?? '/chicken_with_thunder.jpg'}
                alt="chicken with thunder"
              />
            </div>
          </div>
        ))}
      </div>
      <div className={` flex flex-col items-center mx-10`}>
        <Link
          href={'/methodology'}
          className={`bg-white shadow-[0_4px_0_0_black] rounded-md
            cursor-pointer font-black text-brown text-sm tracking-widest
            lg:w-full max-w-screen-xl w-[420px] p-4 m-4 text-center`}
        >
          {t('Results.link')}
        </Link>
      </div>
    </section>
  );
}
