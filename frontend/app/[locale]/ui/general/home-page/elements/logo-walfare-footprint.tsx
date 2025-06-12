import { getI18n } from '@/locales/server';

export default async function Logo() {
  const t = await getI18n();

  return (
    <div className="gap-2 md:gap-1 flex  md:flex-row items-center flex-wrap md:p-2 sm:px-16 font-mono font-black uppercase">
      <p className="px-2 bg-red-300 rounded-full hover:bg-red-400 transition-colors shadow-[0_5px_0px_rgb(0,0,0)]">
        {t('btn_imprint_sffering.imprint')}
      </p>
      <p className="px-2 bg-[#B5ABFF] rounded-full hover:bg-[#8374fF] transition-colors shadow-[0_5px_0px_rgb(0,0,0)]">
        {t('btn_imprint_sffering.suffering')}
      </p>
    </div>
  );
}
