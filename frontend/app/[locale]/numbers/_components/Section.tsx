import type { ReactNode } from 'react';

type Props = {
  className?: string;
  contentClassName?: string;
  title: string;
  text: string;
  children?: ReactNode;
};

export default async function Section({ className, contentClassName, title, text, children }: Props) {
  return (
    <div className={`w-full flex flex-row justify-center ${className}`}>
      <div className="w-full h-full flex flex-col lg:flex-row max-w-6xl gap-8 items-center">
        <div className="w-full lg:w-2/5">
          <h3 className="text-2xl font-bold mb-4">{title}</h3>
          <p className="mb-4">{text}</p>
        </div>
        <div className={`w-full h-full lg:w-3/5 flex justify-center items-center overflow-hidden ${contentClassName}`}>
          {children}
        </div>
      </div>
    </div>
  );
}