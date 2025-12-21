'use client';

import { usePathname } from 'next/navigation';
import clsx from 'clsx';
import useLangSuffix from '@/app/[locale]/ui/_hooks/useLangSuffix';
import matchPath from '@/app/[locale]/ui/_utils/matchPath';

export default function NavClass({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const langSuffix = useLangSuffix();

  // Apply a different background depending on route
  const navClass = clsx('flex flex-row justify-between items-center w-full pl-6 md:pl-2 lg:pl-6 py-2', {
    'bg-pink-2': matchPath('/', pathname, langSuffix),
    'bg-violet': matchPath('/methodology', pathname, langSuffix),
    'bg-white': ['/calculator', '/numbers', '/about', '/legal-notice'].some((routeName) =>
      matchPath(routeName, pathname, langSuffix)
    ),
  });

  return <nav className={navClass}>{children}</nav>;
}
