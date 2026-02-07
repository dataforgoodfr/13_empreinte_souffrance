import type { ReactNode } from 'react';

type Props = {
  className?: string;
  contentClassName?: string;
  title: string;
  text: string;
  children?: ReactNode;
};

export default async function MapSection({ className, title, text, children }: Readonly<Props>) {
  return (
    <div className={`w-full p-section  flex flex-row justify-center items-center ${className}`}>
      <div className="w-full  min-h-[80dvh] flex flex-row gap-8 items-center justify-center ">
        
          <div className="w-full  lg:w-2/5">
            <h3 className="text-2xl font-bold mb-4">{title}</h3>
            <p className="">{text}</p>
          </div>
        
        <div className={`w-full h-full flex justify-end  overflow-hidden `}>
          {children}
        </div>
      </div>
    </div>
  );
}
