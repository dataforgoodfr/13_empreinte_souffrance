'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import clsx from 'clsx';

const links = [
  { name: 'The Figures', href: '/figures' },
  { name: 'Science', href: '/science' },
  { name: 'Life of a chicken', href: '/chicken-life' },
  { name: 'Act now', href: '/act-now' },
  { name: 'About us', href: '/about' },
];

export default function NavLinks() {
  const pathname = usePathname();

  return (
    <>
      {links.map((link) => {
        return (
          <Link
            key={link.name}
            href={link.href}
            className={clsx(
              'flex h-[48px] grow items-center justify-center gap-2 rounded-md bg-gray-50 p-3 text-sm font-medium hover:bg-sky-100 hover:text-blue-600 md:flex-none md:justify-start md:p-2 md:px-3 text-gray-700',
              {
                'bg-sky-200 text-blue-600': pathname == link.href,
              }
            )}
          >
            <p className="hidden md:block">{link.name}</p>
          </Link>
        );
      })}
    </>
  );
}
