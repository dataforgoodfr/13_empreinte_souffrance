import { getI18n } from '@/locales/server';

import NavLinks from '@/app/[locale]/ui/_components/nav-links';
import NavClass from '../_components/nav-class';
import Logo from '../_components/logo-walfare-footprint';
import BurgerMenu from '@/app/[locale]/ui/_components/BurgerMenu';

export default async function Navbar() {
  const t = await getI18n();

  const links = [
    { name: t('NavBarLink.presentation'), href: '/' },
    { name: t('NavBarLink.methodology'), href: '/methodology' },
    { name: t('NavBarLink.calculator'), href: '/calculator' },
    { name: t('NavBarLink.numbers'), href: '/numbers' },
    { name: t('NavBarLink.about'), href: '/about' },
  ];

  return (
    <NavClass>
      <Logo />
      <div className="hidden md:flex flex-row items-center mr-16">
        <NavLinks links={links} />
      </div>
      <BurgerMenu className="md:hidden">
        <NavLinks links={links} isVertical={true} />
      </BurgerMenu>
    </NavClass>
  );
}
