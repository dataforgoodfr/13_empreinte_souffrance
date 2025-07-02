import { getI18n } from '@/locales/server';
import Link from 'next/link';

export default async function Logo() {
  const t = await getI18n();

  return (
    <Link
      href="/"
      className="gap-2 md:gap-1 flex  md:flex-row items-center flex-wrap md:p-2  font-mono text-xl font-black uppercase"
    >
      <img src="/logo_WF.png" className="w-[40px] "/>
        
      < h1 className="  ">
        {t('btn_imprint_sffering.imprint')}
      </h1 >
      <h1 className="">
        {t('btn_imprint_sffering.suffering')}
      </h1>
    </Link>
  );
}
