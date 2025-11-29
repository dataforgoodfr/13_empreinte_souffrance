import { ReactNode } from 'react';
import Thunder from '@/app/[locale]/ui/_components/BoltIconV2';
import Link from 'next/link';

type Props = {
  superTitle?: ReactNode;
  title?: ReactNode;
  children?: ReactNode;
  source?: { url: string; name: ReactNode };
};

export default function InfoContent({ superTitle, title, children, source }: Props) {
  return (
    <div className={`w-full h-full flex gap-3 flex-col p-2 justify-start lg:justify-between`}>
      <div className={`w-full flex flex-col lg:flex-row`}>
        <Thunder className={'mr-7 my-2 text-pink-3 '} />
        <div className={`flex flex-col`}>
          <div className={`text-md font-bold whitespace-pre-line`}>{superTitle}</div>
          <div className={`text-3xl font-black whitespace-pre-line`}>{title}</div>
        </div>
      </div>
      <div className={`font-semibold text-lg`}>{children}</div>
      <div className="w-full">
        <Link
          href={source?.url!}
          className="inline-block py-1 pl-4 bg-grey hover:bg-violet w-full font-mono dark-text tracking-wider transition-all duration-200 align-middle border-b border-brown underline"
        >
          {source?.name}
        </Link>
      </div>
    </div>
  );
}
