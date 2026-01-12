import Link from 'next/link';
import Image from 'next/image';

export default async function Logo() {
  return (
    <Link href="/" className="shrink-0">
      <Image
        src="/logotype-heure-comptes.svg"
        width={215}
        height={50}
        alt="Logo Anima"
        className="object-contain w-48 min-h-12"
      />
    </Link>
  );
}
