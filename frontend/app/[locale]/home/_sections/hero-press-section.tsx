import { getI18n } from '@/locales/server';
import Image from 'next/image';
import ArrowDown from '@/app/[locale]/ui/_logo/ArrowDown';


export default async function HeroPressSection() {
  const t = await getI18n();

  return (
    <header className="relative flex flex-col items-center justify-between w-full overflow-hidden bg-gradient-to-b from-pink-2 to-pink-3">
      <div className="flex flex-col items-center justify-center flex-grow pt-2">
        <Image
          src="/full-bars_egg.svg"
          width={200}
          height={200}
          alt="egg shaped logo with a hen behind bars"
          className="mb-0 md:mb-0"
        />
        <h1 className="text-center font-bold text-lg md:text-sm leading-snug text-black px-4 mt-[-1rem] mx-10 sm:mx-25 md:mx-45">
          {t('PressSection.ten_years_ago_supermarkets_pledged').toUpperCase()}{' '}
          <span className="underline">{t('PressSection.to_ban_eggs_from_caged_hens_by_2026').toUpperCase()}.</span>
        </h1>
      </div>

      <div className="w-full relative">
        <div className="w-full sm:flex hidden justify-center ">
          <Image
            src="/press-articles.png"
            width={1650}
            height={1350}
            alt="collage of press articles"
            className="w-full block"
          />
        </div>
        <div className="w-full sm:hidden flex justify-center">
          <Image
            src="/press-articles_mobile.png"
            width={1650}
            height={1350}
            alt="collage of press articles"
            className="w-full"
          />
        </div>
        <div className="absolute inset-0 bg-gradient-to-t from-white/40 to-transparent"></div>
      </div>
      <span className="absolute bottom-0">
        <ArrowDown />
      </span>
    </header>
  );
}
