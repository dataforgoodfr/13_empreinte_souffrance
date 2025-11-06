'use client';

import { usePathname } from 'next/navigation';
import clsx from 'clsx';

export default function NavClass({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();

  // Applique un fond différent selon la route
  const navClass = clsx('flex flex-row justify-between w-full h-full', {
    'bg-pink-2': pathname === '/fr' || pathname === '/',
    'bg-violet': pathname === '/fr/methodology' || pathname === '/methodology',
    'bg-white':
      pathname === '/fr/calculator' ||
      pathname === '/calculator' ||
      pathname === '/fr/numbers' ||
      pathname === '/numbers' ||
      pathname === '/fr/about' ||
      pathname === '/about',
  });

  return <nav className={navClass}>{children}</nav>;
}
