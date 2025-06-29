'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import clsx from 'clsx';

export default function NavLinks({ links }: { links: { name: string; href: string }[] }) {
  const pathname = usePathname();

  return (
      <nav
          className="flex justify-center items-center md:justify-end gap-8 md:gap-4 font-mono font-black uppercase text-sm flex-grow basis-0 min-w-0 max-h-4">
        {links.map((link) => {
          const isActive = pathname.startsWith(`/fr${link.href}`) || pathname.startsWith(link.href);

          return (
              <Link
                  key={link.name}
                  href={link.href}
                  className={clsx(
                      'flex h-[48px] items-center justify-center px-2 md:p-3 text-sm font-medium text-gray-700 hover:underline underline-offset-4 decoration-[#FF7B7B] decoration-2',
                      {
                        'underline underline-offset-4': isActive,
                      }
                  )}
              >
                <p>{link.name}</p>
              </Link>
          );
        })}
      </nav>
  );
}
