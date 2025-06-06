import { getScopedI18n } from '@/locales/server';

export default async function HeroSection() {
  const scopedT = await getScopedI18n('HeroSection');
  // const title = scopedT('title');

  return (
    <header className="relative h-screen w-full overflow-hidden flex items-center justify-end">
      {/* Image de fond */}
      <img
        src="chicken_header.png"
        alt=""
        className="absolute inset-0 object-cover object-right transform scale-[1.3] origin-top-right"
      />

      {/* Contenu à gauche */}
      <hgroup className="relative  flex flex-col justify-center items-start text-left p-4 max-w-[40rem]">
        <h1 className="text-6xl font-bold">
          <span className="px-2 flex flex-wrap">
            <ColorText lettre="C" color="#FFE9E9" />
            <ColorText lettre="o" color="#FFC3C3" />
            <ColorText lettre="m" color="#FF7B7B" />
            <ColorText lettre="b" color="#FFC3C3" />
            <ColorText lettre="i" color="#FFC3C3" />
            <ColorText lettre="e" color="#FF7B7B" />
            <ColorText lettre="n" color="#FF7B7B" />
            <ColorText lettre="?" color="#B5ABFF" />
          </span>
        </h1>
        <p className="mt-4  text-[#FFE9E9] uppercase">
          <span className=" text-4xl font-bold">{scopedT('title_sentence.strong1')}</span>
          <span className=" text-4xl">{scopedT('title_sentence.part1')}</span>
          <span className=" text-4xl font-bold">{scopedT('title_sentence.strong2')}</span>
          <br />
          <span className=" text-4xl">{scopedT('title_sentence.part2')}</span>
          <span className=" text-4xl font-bold">{scopedT('title_sentence.strong3')}</span>
        </p>
        <img src="/arrow_down.png" alt="Flèche vers le bas" className="mt-10 w-10 h-10 animate-bounce" />
      </hgroup>
    </header>
  );
}

interface colorText {
  lettre: string;
  color: string;
}

function ColorText({ lettre, color }: colorText) {
  return (
    <div
      style={{ backgroundColor: color }}
      className="inline-flex items-center justify-center h-28 md:w-14 text-6xl text-[#3C0A0A] rounded-[9999px] mx-[2px] uppercase font-mono font-extralight shadow-[0_10px_0px_rgb(0,0,0)]"
    >
      {lettre}
    </div>
  );
}
