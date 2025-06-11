import { getI18n } from '@/locales/server';

import Link from 'next/link';
import { LocaleSelect } from '../localselect';
import BtnImprintSuffering from './home-page/elements/btn-imprint-suffering';

export default async function Navbar() {
  const t = await getI18n();

  return (
    <>
      <header className="flex  w-max-full justify-between items-center  bg-red-50 p-4  ">
        <nav className="flex justify-between items-center md:w-full md:gap-2 ">
          <BtnImprintSuffering />

          <div className="flex flex-col sm:flex-row justify-around items-center md:items-end p-2 md:gap-6 font-mono font-black uppercase">
            {/* todo add links to the navbar */}
            <Link
              href={''}
              className="hover:bg-gray-200 rounded-full px-3 transition-colors duration-150 ease-in-out tracking-wider"
            >
              {t('Navbar.link1')}
            </Link>
            {/* todo add links to the navbar */}
            <Link href={''} className="hover:bg-gray-200 rounded-full px-3 transition tracking-wider">
              {t('Navbar.link2')}
            </Link>
          </div>
        </nav>
        <LocaleSelect />
      </header>
    </>
  );
}
