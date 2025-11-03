// import { getI18n } from '@/locales/server';
// import clsx from 'clsx';
import Image from 'next/image';

export default async function HeroPressSection() {
  // const t = await getI18n();

  return (
    <header className="relative flex flex-col items-center justify-between w-full overflow-hidden bg-gradient-to-b from-pink-2 to-pink-3">
      <div className="flex flex-col items-center justify-center flex-grow pt-2">
        <Image
          src="/full-bars_egg.svg"
          width={200}
          height={200}
          alt="egg shaped logo with a hen behind bars"
          className="mb-0 md:mb-0"
        />
        <h1 className="text-center font-bold text-lg md:text-sm leading-snug text-black px-4 mt-[-1rem] mx-10 sm:mx-25 md:mx-45">
          IL Y A 10 ANS, LES SUPERMARCHÉS S’ENGAGEAIENT{' '}
          <span className="underline">À BANNIR LES ŒUFS DE POULES EN CAGE AVANT 2026.</span>
        </h1>
      </div>

      <div className="w-full sm:flex hidden justify-center">
        <Image
          src="/press-articles.png"
          width={1650}
          height={1350}
          alt="collage of press articles"
          className="w-full"
        />
      </div>
      <div className="w-full sm:hidden flex justify-center">
        <Image
          src="/press-articles_mobile.png"
          width={1650}
          height={1350}
          alt="collage of press articles"
          className="w-full"
        />
      </div>
    </header>
  );
}
