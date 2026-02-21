import clsx from 'clsx';
import Image from 'next/image';
import { ReactNode } from 'react';

type SectionTitleProps = {
  image_path: string;
  image_alt: string;
  title: ReactNode | string;
  text_color?: 'white' | 'black';
};

export default function SectionTitle({ image_path, image_alt, title, text_color = 'black' }: SectionTitleProps) {
  return (
    <div className="flex flex-col items-center justify-center flex-grow pt-2">
      <Image src={image_path} width={200} height={200} alt={image_alt} className="mb-0 md:mb-0" />
      <h2
        className={clsx(
          'text-center text-lg md:text-sm leading-snug px-4 mt-[-2.5rem] sm:mx-25 md:mx-45 uppercase max-w-[900px]',
          {
            'text-black': text_color === 'black',
            'text-white': text_color === 'white',
          }
        )}
      >
        {title}
      </h2>
    </div>
  );
}
