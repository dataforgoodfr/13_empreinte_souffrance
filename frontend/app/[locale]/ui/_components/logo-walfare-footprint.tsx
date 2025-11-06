import { getI18n } from '@/locales/server';
import Link from 'next/link';
import EmpreinteSouffrance from '@/app/[locale]/ui/_logo/EmpreinteSouffrance';

export default async function Logo() {
  const t = await getI18n();

  return (
    <Link
      href="/"
      className="gap-2 md:gap-1 flex md:flex-row items-center md:p-2 text-bold text-black uppercase"
    >
      <EmpreinteSouffrance className="text-black w-10 h-12" />
      <p className="flex flex-col text-xl/4 text-black font-bold">
        <span>{t('time_for_reckoning_logo.time')}</span>
        <span>{t('time_for_reckoning_logo.for')}{" "}{t('time_for_reckoning_logo.reckoning')}</span>
      </p>
    </Link>
  );
}
