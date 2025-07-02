import { getI18n } from '@/locales/server';

import NavLinks from '@/app/[locale]/ui/general/elements/nav-links';
import { LocaleSelect } from '../localselect';
import Logo from './home-page/elements/logo-walfare-footprint';

export default async function Navbar() {
  const t = await getI18n();

    const links= [
    { name: t('NavBarLink.methodology'), href: '/methodology' },
    { name: t('NavBarLink.calculator'), href: '/calculator' },
    { name: t('NavBarLink.about'), href: '/about' },
  ];

  return (
    <>
      <header className="bg-white px-4 w-full">
        <div className="flex flex-col md:flex-row md:items-center md:justify-between w-full gap-4">
          <div className="relative flex justify-between md:justify-start items-center w-full">
            <div className="flex justify-start items-center">
              <Logo/>
            </div>
            <div className="grow mr-20 hidden md:block">
              <NavLinks links={links}/>
            </div>
            <div className="absolute right-0">
              <LocaleSelect/>
            </div>
          </div>
          <div className="grow block md:hidden">
            <NavLinks links={links}/>
          </div>
        </div>
      </header>
    </>
  );
}
