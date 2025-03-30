'use client';

import './globals.css';
import { useEffect } from 'react';

export default function Error({ error, reset }: { error: Error & { digest?: string }; reset: () => void }) {
  useEffect(() => {
    console.error(error);
  }, [error]);

  return (
    <section
      className="w-full bg-gradient-to-r from-blue-600 via-blue-500 to-indigo-500 h-screen flex items-center justify-around px-8 sm:px-16"
      style={{ backgroundColor: 'red' }}
    >
      <div>
        <h2>Something went wrong!</h2>
        <button className="bg-indigo-800 rounded-lg p-2 cursor-pointer" onClick={() => reset()}>
          Try again
        </button>
      </div>
    </section>
  );
}
