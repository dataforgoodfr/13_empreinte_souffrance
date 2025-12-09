import Link from 'next/link';
import Image from 'next/image';

export default async function Logo() {
  return (
    <Link href="/" className="gap-2 md:gap-1 flex md:flex-row items-center md:p-2 text-bold text-black uppercase">
      <Image src="/logotype.svg" width={215} height={50} alt="Logo Anima" className="mb-0 md:mb-0 object-contain" />
    </Link>
  );
}
