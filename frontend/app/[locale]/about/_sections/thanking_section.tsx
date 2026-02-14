import { getScopedI18n } from '@/locales/server';
import Image from 'next/image';

export default async function ThankingSection() {
  const scopedT = await getScopedI18n('aboutPage');

  return (
    <section className="p-section flex justify-center text-black gap-[28px]">
      <div className="max-w-contain flex flex-col items-center gap-6">
        <Image src="/heart_icon.svg" width={70} height={70} alt="heart icon" className="mb-0 md:mb-0" />
        <p className="lg:max-w-2/3 text-body">{scopedT('thanking_section')}</p>
      </div>
    </section>
  );
}
