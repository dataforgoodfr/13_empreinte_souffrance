import Image from 'next/image';
import { ReactNode } from 'react';

type SectionTitleProps = {
  image_path: string;
  image_alt: string;
  title: ReactNode;
};

export default function SectionTitle({ image_path, image_alt, title }: SectionTitleProps) {
  return (
    <div className="flex flex-col items-center justify-center flex-grow pt-2">
      <Image src={image_path} width={200} height={200} alt={image_alt} className="mb-0 md:mb-0" />
      <h1 className="text-center font-bold text-lg md:text-sm leading-snug text-black px-4 mt-[-1rem] mx-10 sm:mx-25 md:mx-45">
        {title}
      </h1>
    </div>
  );
}
