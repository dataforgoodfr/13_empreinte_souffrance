import { getI18n } from '@/locales/server';

import NavLinks from "@/app/[locale]/ui/general/elements/nav-links";
import { LocaleSelect } from '../localselect';
import BtnImprintSuffering from './elements/btn-imprint-suffering';


export default async function Navbar() {
  const t = await getI18n();




  return (
    <>
      <header className="bg-red-50 p-1 w-full h-full flex flex-col md:flex-row md:items-center md:justify-between w-full gap-4">
          {/* Ligne du haut : gauche = boutons + langue en mobile / boutons seul en desktop */}
          <div className="flex justify-between md:justify-start items-center gap-2 w-full md:w-auto">
              <BtnImprintSuffering />
            {/* Ce bloc est visible en mobile seulement */}
            <div className="md:hidden">
              <LocaleSelect />
            </div>
          </div>

          {/* Centre : liens */}
          <nav className="flex justify-center items-center md:justify-end gap-4 font-mono font-black uppercase text-sm flex-grow basis-0 min-w-0">
         <NavLinks key={t} />
          </nav>

          {/* Droite : sélecteur de langue visible en desktop seulement */}
          <div className="hidden md:flex justify-end">
            <LocaleSelect />
          </div>
      </header>
    </>
  );
}
