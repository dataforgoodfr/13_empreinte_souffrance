import { getI18n } from '@/locales/server';
import Image from 'next/image';

export default async function HumanFoodSection() {
  const t = await getI18n();

  return (
    <section className="bg-indigo-800 h-screen p-8 sm:px-16">
      <div className="w-full">
        <h1 className="w-full text-5xl sm:text-6xl lg:text-7xl font-bold text-white text-center">
          <span className="text-green-300">text</span>
          &nbsp;text
        </h1>
      </div>
      <div className="w-full flex items-center justify-between">
        <div className="max-w-xl space-y-6">
          <p className="text-2xl text-white">{t('welfare_footprint_institute')}</p>
        </div>
        <div className="hidden lg:block">
          <Image src="/tmp_chicken-image.webp" width={560} height={620} className="block" alt="Picture of a chicken" />
        </div>
      </div>
    </section>
  );
}
