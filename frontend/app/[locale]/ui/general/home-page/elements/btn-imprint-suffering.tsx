import { getI18n } from '@/locales/server';
import Link from 'next/link';

export default async function BtnImprintSuffering() {
  const t = await getI18n();

  return (
    <div className="gap-1 flex  items-center flex-wrap p-8 sm:px-16">
      {/* todo add links to the navbar */}
      <Link
        href={''}
        className=" font-mono font-black uppercase  px-2 bg-red-300 rounded-full hover:bg-red-400 transition-colors shadow-[0_5px_0px_rgb(0,0,0)]"
      >
        {t('btn_imprint_sffering.imprint')}
      </Link>
      {/* todo add links to the navbar */}
      <Link
        href={''}
        className=" font-mono font-black uppercase px-2 bg-[#B5ABFF] rounded-full hover:bg-[#8374fF] transition-colors shadow-[0_5px_0px_rgb(0,0,0)]"
      >
        {t('btn_imprint_sffering.suffering')}
      </Link>
    </div>
  );
}
