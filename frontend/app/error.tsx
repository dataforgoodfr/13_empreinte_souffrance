'use client';

import './globals.css';
import Link from 'next/link';

export default function Error({ reset }: { reset: () => void }) {
  return (
    <section className="w-full bg-gradient-to-r from-blue-600 via-blue-500 to-indigo-500 h-screen flex items-center justify-around px-8 sm:px-16">
      <div className="max-w-xl space-y-6 flex flex-col">
        <div className="inline-block bg-indigo-800 text-white py-2 px-4 rounded-lg text-sm font-semibold tracking-wide w-max">
          🐣🐥🐤🐔
        </div>
        <h1 className="text-5xl sm:text-6xl lg:text-7xl font-bold text-white">Something went wrong!</h1>

        <Link href="/" className="bg-indigo-800 rounded-lg p-2 w-max">
          Return home
        </Link>
        <button className="bg-indigo-800 rounded-lg p-2 cursor-pointer w-max" onClick={() => reset()}>
          Try again
        </button>
      </div>
    </section>
  );
}
