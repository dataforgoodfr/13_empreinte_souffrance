'use client';

import { usePathname } from 'next/navigation';
import clsx from 'clsx';
import useLangSuffix from '@/app/[locale]/ui/_hooks/useLangSuffix';
import matchPath from '@/app/[locale]/ui/_utils/matchPath';

export default function NavClass({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const langSuffix = useLangSuffix();
  // Apply a different background depending on route
  const navClass = clsx('flex flex-row justify-between w-full h-full', {
    'bg-pink-2': matchPath('/', pathname, langSuffix),
    'bg-violet': matchPath('/methodology', pathname, langSuffix),
    'bg-white': ['/calculator', '/numbers', '/about'].some((routeName) => matchPath(routeName, pathname, langSuffix)),
  });

  return <nav className={navClass}>{children}</nav>;
}
