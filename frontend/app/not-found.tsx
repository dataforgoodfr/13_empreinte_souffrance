import Link from 'next/link';
import './globals.css';

export default async function NotFound() {
  return (
    <section className="w-full bg-gradient-to-r from-blue-600 via-blue-500 to-indigo-500 h-screen flex items-center justify-around px-8 sm:px-16">
      <div className="max-w-xl space-y-6">
        <div className="inline-block bg-indigo-800 text-white py-2 px-4 rounded-lg text-sm font-semibold tracking-wide">
          🐣🐥🐤🐔
        </div>
        <h1 className="text-5xl sm:text-6xl lg:text-7xl font-bold text-white">Not Found</h1>
        <p className="text-xl sm:text-2xl font-bold text-white">Could not find requested resource</p>

        <Link href="/" className="bg-indigo-800 rounded-lg p-2 text-white">
          Return Home
        </Link>
      </div>
    </section>
  );
}
