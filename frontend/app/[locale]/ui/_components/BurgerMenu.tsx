'use client';

import React, { useRef, useState } from 'react';

type Props = {
  children: React.ReactNode;
  className?: string;
};

export default function BurgerMenu({ children, className }: Props) {
  const [open, setOpen] = useState(false);
  const menuRef = useRef<HTMLDivElement>(null);

  const handleToggle = () => {
    setOpen((prev) => !prev);
  };

  const handleClose = () => {
    setOpen(false);
  };

  return (
    <div className={className}>
      <div ref={menuRef} className={`relative z-20 h-[48px]`}>
        <button
          onClick={handleToggle}
          className="bg-transparent border-none p-0 cursor-pointer outline-none h-full"
          aria-label={open ? 'Close menu' : 'Open menu'}
        >
          <div className="flex flex-col items-center justify-center gap-1 h-full w-[36px]">
            <span
              className={`block h-[4px] bg-gray-800 rounded origin-center transition-all duration-300 ${
                open ? 'w-[28px] rotate-45 translate-y-[8px] translate-x-[2px]' : 'w-[30px]'
              }`}
            />
            <span
              className={`block w-[30px] h-[4px] bg-gray-800 rounded transition-opacity duration-300 ${
                open ? 'opacity-0' : 'opacity-100'
              }`}
            />
            <span
              className={`block h-[4px] bg-gray-800 rounded origin-center transition-all duration-300 ${
                open ? 'w-[28px] -rotate-45 -translate-y-[8px] translate-x-[2px]' : 'w-[30px]'
              }`}
            />
          </div>
        </button>

        <div
          className={`absolute top-full right-0 bg-white border border-gray-200 shadow-lg rounded-lg overflow-hidden transition-all duration-300 ease-out
          ${open ? 'max-h-[500px] opacity-100' : 'max-h-0 opacity-0'}
          flex flex-col gap-2 p-4`}
          style={{ minWidth: '200px' }}
        >
          {children}
        </div>
      </div>

      {open && <div className="fixed inset-0 bg-transparent z-10" onClick={handleClose} />}
    </div>
  );
}
