import EggInterrogation from '@/app/[locale]/numbers/_components/EggInterrogation';

export default async function Header() {
  return (
    <div className="w-full flex flex-col items-center">
      <EggInterrogation />
      <h1 className="relative z-10 text-center font-albert-sans font-black text-brown" style={{ top: '-4rem' }}>
        {'Les chiffres derrière l’histoire'}
      </h1>
    </div>
  );
}