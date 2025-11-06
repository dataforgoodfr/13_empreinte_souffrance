'use client';

import { usePathname } from 'next/navigation';
import clsx from 'clsx';

export default function NavClass({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();

  // Applique un fond différent selon la route
  const navClass = clsx('flex flex-row justify-between w-full h-full', {
    'bg-pink-2': pathname === '/fr' || pathname === '/en',
    'bg-violet': pathname === '/fr/methodology' || pathname === '/en/methodology',
    'bg-white':
      pathname === '/fr/calculator' ||
      pathname === '/en/calculator' ||
      pathname === '/fr/numbers' ||
      pathname === '/en/numbers' ||
      pathname === '/fr/about' ||
      pathname === '/en/about',
  });

  return <nav className={navClass}>{children}</nav>;
}
