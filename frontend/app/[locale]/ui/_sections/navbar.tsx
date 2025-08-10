import { getI18n } from '@/locales/server';

import NavLinks from '@/app/[locale]/ui/_components/nav-links';
import Logo from '../_components/logo-walfare-footprint';
import { LocaleSelect } from '@/app/[locale]/ui/_components/localselect';
import BurgerMenu from '@/app/[locale]/ui/_components/BurgerMenu';

export default async function Navbar() {
  const t = await getI18n();

  const links = [
    { name: t('NavBarLink.presentation'), href: '/' },
    { name: t('NavBarLink.methodology'), href: '/methodology' },
    { name: t('NavBarLink.calculator'), href: '/calculator' },
    { name: t('NavBarLink.about'), href: '/about' },
  ];

  return (
    <>
      <Logo />
      <div className="hidden lg:flex flex-row items-center">
        <NavLinks links={links} />
        <LocaleSelect />
      </div>
      <BurgerMenu className="lg:hidden">
        <NavLinks links={links} isVertical={true} />
        <LocaleSelect />
      </BurgerMenu>
    </>
  );
}
