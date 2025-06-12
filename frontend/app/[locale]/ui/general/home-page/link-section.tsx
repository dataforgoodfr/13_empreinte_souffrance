import { getI18n } from '@/locales/server';
import Link from 'next/link';

export default async function LinkSection() {
  const t = await getI18n();
  //todo replace "#" to reel links
  const firstLine = [
    [t('LinkSection.link1'), '#'],
    [t('LinkSection.link2'), '#'],
    [t('LinkSection.link3'), '#'],
  ];

  const secondLine = [
    [t('LinkSection.link4'), '#'],
    [t('LinkSection.link5'), '#'],
    [t('LinkSection.link6'), '#'],
  ];

  const linkStyle =
    ' py-2 text-center font-mono tracking-widest text-[#3b0a0a] border border-red-300 hover:bg-gray-200 md:grow md:text-nowrap';

  return (
    <section className="w-full bg-white flex flex-col items-center justify-center">
      {[firstLine, secondLine].map((line, index) => (
        <div key={index} className="flex w-full">
          {line.map(([text, href]) => (
            <Link key={text} href={href} className={linkStyle}>
              {text}
            </Link>
          ))}
        </div>
      ))}
    </section>
  );
}
