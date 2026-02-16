import type { ReactNode } from 'react';

type Props = {
  className?: string;
  innerClassName?: string;
  contentClassName?: string;
  title: string;
  text: ReactNode;
  anchorName?: string;
  children?: ReactNode;
};

export default async function Section({ className, innerClassName, contentClassName, title, text, anchorName, children }: Readonly<Props>) {
  return (
    <div className={`w-full p-section flex flex-row justify-center items-center ${className ?? ''}`} id={anchorName}>
      <div className={`w-full min-h-[80dvh] flex flex-col lg:flex-row gap-8 items-center justify-center ${innerClassName ?? 'max-w-6xl'}`}>
        <div className="w-full lg:w-2/4">
          <h3 className="text-2xl font-bold mb-4">{title}</h3>
          <p className="">{text}</p>
        </div>
        <div className={`w-full h-full flex overflow-hidden ${contentClassName ?? 'lg:w-3/5 justify-center items-center'}`}>
          {children}
        </div>
      </div>
    </div>
  );
}