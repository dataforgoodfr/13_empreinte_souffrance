import { getI18n } from '@/locales/server';

import Link from 'next/link';
import { LocaleSelect } from '../localselect';
import BtnImprintSuffering from './home-page/elements/btn-imprint-suffering';

export default async function Navbar() {
  const t = await getI18n();

  return (
    <>
      <header className="flex justify-between items-center">
        <nav className="flex justify-between items-center w-full">
          <BtnImprintSuffering />
          <div className="flex justify-around items-center px-4 py-2 gap-6">
            {/* todo add links to the navbar */}
            <Link href={''} className="hover:bg-gray-200">
              {t('Navbar.link1')}
            </Link>
            {/* todo add links to the navbar */}
            <Link href={''} className="">
              {t('Navbar.link2')}
            </Link>
          </div>
        </nav>
        <LocaleSelect />
      </header>
    </>
  );
}
