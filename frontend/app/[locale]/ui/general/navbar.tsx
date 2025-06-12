import { getI18n } from '@/locales/server';

import Link from 'next/link';
import { LocaleSelect } from '../localselect';
import Logo from './home-page/elements/logo-walfare-footprint';

export default async function Navbar() {
  const t = await getI18n();

  return (
    <>
      <header className="bg-red-50 p-4 w-full">
        <div className="flex flex-col md:flex-row md:items-center md:justify-between w-full gap-4">
          {/* Ligne du haut : gauche = boutons + langue en mobile / boutons seul en desktop */}
          <div className="flex justify-between md:justify-start items-center gap-2 w-full md:w-auto">
            <div className="flex justify-start items-center gap-2">
              <Logo />
            </div>
            {/* Ce bloc est visible en mobile seulement */}
            <div className="md:hidden">
              <LocaleSelect />
            </div>
          </div>

          {/* Centre : liens */}
          <div className="flex justify-center items-center md:justify-end gap-4 font-mono font-black uppercase text-sm flex-grow basis-0 min-w-0">
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

          {/* Droite : sélecteur de langue visible en desktop seulement */}
          <div className="hidden md:flex justify-end">
            <LocaleSelect />
          </div>
        </div>
      </header>
    </>
  );
}
