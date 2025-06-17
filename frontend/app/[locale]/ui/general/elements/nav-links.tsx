'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import clsx from 'clsx';

export default function NavLinks({ links }: { links: { name: string; href: string }[] }) {
  const pathname = usePathname();

  return (
    <>
      {links.map((link) => {
        const isActive = pathname.startsWith(`/fr${link.href}`) || pathname.startsWith(link.href);

        return (
          <Link
            key={link.name}
            href={link.href}
            className={clsx(
              'flex h-[48px] grow items-center justify-center gap-2 rounded-md p-3 text-sm font-medium  md:flex-none md:justify-start md:p-2 md:px-3 text-gray-700 hover:underline underline-offset-4',
              {
                'underline underline-offset-4': isActive,
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
