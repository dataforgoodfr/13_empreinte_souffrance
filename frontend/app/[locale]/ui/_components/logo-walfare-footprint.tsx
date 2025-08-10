import { getI18n } from '@/locales/server';
import Link from 'next/link';
import EmpreinteSouffrance from '@/app/[locale]/ui/logo/EmpreinteSouffrance';

export default async function Logo() {
  const t = await getI18n();

  return (
    <Link
      href="/"
      className="gap-2 md:gap-1 flex md:flex-row items-center flex-wrap md:p-2  font-mono text-xl font-black uppercase h-16"
    >
      <EmpreinteSouffrance className="text-brown w-10 h-12" />
      <p className="flex flex-col leading-4 text-xl text-brown">
        <span>{t('btn_imprint_sffering.imprint')}</span>
        <span>{t('btn_imprint_sffering.suffering')}</span>
      </p>
    </Link>
  );
}
