'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import clsx from 'clsx';
import useLangSuffix from '@/app/[locale]/ui/_hooks/useLangSuffix';
import matchPath from '@/app/[locale]/ui/_utils/matchPath';

type Props = {
  links: { name: string; href: string }[];
  isVertical?: boolean;
};

export default function NavLinks({ links, isVertical: passedIsVertical }: Props) {
  const isVertical = passedIsVertical ?? false;

  const pathname = usePathname();
  const langSuffix = useLangSuffix();

  return (
    <nav
      className={`
        flex flex-${isVertical ? 'col' : 'row'} justify-center items-center md:justify-end min-w-0
        gap-8 md:gap-4 font-mono font-black
        text-sm text-black
      `}
    >
      {links.map((link) => {
        const isActive = matchPath(link.href, pathname, langSuffix);

        return (
          <Link
            key={link.name}
            href={link.href}
            className={clsx(
              'flex flex-row h-[48px] items-center justify-center ' +
                'px-2 md:p-3 text-[.875rem] dark-text font-bold tracking-[.14em] antialiased text-nowrap ' +
                'hover:underline underline-offset-4 decoration-[#FF7B7B] decoration-2',
              {
                'underline underline-offset-4': isActive,
              }
            )}
          >
            {link.name}
          </Link>
        );
      })}
    </nav>
  );
}
