import Link from 'next/link';

export default function LinkSection() {
  //todo replace "#" to reel links
  const firstLine = [
    ['LE WELFARE FOOTPRINT INSTITUTE', '#'],
    ['DE QUOI SOUFFRENT LES POULES ?', '#'],
    ['L’ÉQUATION DE LA DOULEUR', '#'],
  ];

  const secondLine = [
    ['SON FARDEAU, ENFIN VISIBLE', '#'],
    ['L’EMPREINTE SOUFFRANCE DES ŒUFS', '#'],
    ['ALLER PLUS LOIN', '#'],
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
