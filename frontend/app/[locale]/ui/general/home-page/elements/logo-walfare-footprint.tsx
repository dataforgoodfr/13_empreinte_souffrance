import { getI18n } from '@/locales/server';
import Link from 'next/link';

export default async function Logo() {
  const t = await getI18n();

  return (
    <Link
      href="/"
      className="gap-2 md:gap-1 flex  md:flex-row items-center flex-wrap md:p-2 sm:px-16 font-mono font-black uppercase"
    >
      <p className="px-2 bg-red-300 rounded-full  transition-colors shadow-[0_5px_0px_rgb(0,0,0)]">
        {t('btn_imprint_sffering.imprint')}
      </p>
      <p className="px-2 bg-[#B5ABFF] rounded-full  transition-colors shadow-[0_5px_0px_rgb(0,0,0)]">
        {t('btn_imprint_sffering.suffering')}
      </p>
    </Link>
  );
}
