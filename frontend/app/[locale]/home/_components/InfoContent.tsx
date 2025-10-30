import { ReactNode } from 'react';
import Thunder from '@/app/[locale]/home/_asset/Thunder';
import Link from '@/app/[locale]/home/_components/Link';

type Props = {
  superTitle?: ReactNode;
  title?: ReactNode;
  children?: ReactNode;
  source?: { url: string; name: ReactNode };
};

export default function InfoContent({ superTitle, title, children, source }: Props) {
  return (
    <div className={`w-full h-full flex flex-col p-2 justify-between`}>
      <div className={`w-full flex flex-col lg:flex-row`}>
        <Thunder className={'mr-7 my-2'} />
        <div className={`flex flex-col`}>
          <div className={`text-md font-bold whitespace-pre-line`}>{superTitle}</div>
          <div className={`text-3xl font-black whitespace-pre-line`}>{title}</div>
        </div>
      </div>
      <div className={`font-semibold text-lg`}>{children}</div>
      <Link href={source?.url}>{source?.name}</Link>
    </div>
  );
}
