import { getI18n } from '@/locales/server';

import Link from 'next/link';
import { LocaleSelect } from '../localselect';
import BtnImprintSuffering from './home-page/elements/btn-imprint-suffering';

export default async function Navbar() {
  const t = await getI18n();

  return (
    <>
      <header className="flex flex-col bg-red-50 p-4 w-full">
        {/* add link to redirect */}
        <div className="flex flex-row justify-center items-center gap-2 mb-4 font-mono font-black uppercase">
          <Link href="" className="hover:bg-gray-200 rounded-full px-3 transition tracking-wider">
            {t('Navbar.link1')}
          </Link>
          <Link href="" className="hover:bg-gray-200 rounded-full px-3 transition tracking-wider">
            {t('Navbar.link2')}
          </Link>
          <Link
            href="/about"
            className="hover:bg-gray-200 rounded-full px-3 transition tracking-wider whitespace-nowrap"
          >
            {t('Navbar.link3')}
          </Link>
        </div>

        <div className="flex flex-row justify-between items-center w-full">
          <BtnImprintSuffering />
          <LocaleSelect />
        </div>
      </header>
    </>
  );
}
