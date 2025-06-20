import { getI18n } from '@/locales/server';

export default async function HeroSection() {
  // const t = await getScopedI18n('HeroSection');
  const t = await getI18n();
  const title: string = t('HeroSection.title');

  return (
    <header className="relative h-screen w-full overflow-hidden flex items-center justify-end">
      <img
        src="chicken_header.png"
        alt={t('HeroSection.altPicture')}
        className="absolute inset-0 object-cover object-right transform scale-[1.3] origin-top-right"
      />

      <hgroup className="relative  flex flex-col justify-center items-start text-left p-4 max-w-[40rem]">
        <h1 className="text-5xl font-bold">
          <span className="{t('title_sentence.strong1')} ">
            {/* translation map to add a colored dot on each of the letters to keep the style of the model */}
            {title.split('').map((lettre: string, index: number) => (
              <ColorText key={index} lettre={lettre} color={lettre === ' ' ? 'transparent' : lettreColor()} />
            ))}
          </span>
          <span
            style={{ backgroundColor: '#B5ABFF' }}
            className="inline-flex items-center justify-center h-28 md:w-14 text-5xl text-[#3C0A0A] rounded-[9999px] mx-[2px] uppercase font-mono font-extralight shadow-[0_10px_0px_rgb(0,0,0)]"
          >
            ?
          </span>
        </h1>
        <p className="mt-4 text-[#FFE9E9] uppercase">
          <span className="text-4xl font-bold">{t('HeroSection.title_sentence.strong1')}</span>
          <span className="text-4xl">{t('HeroSection.title_sentence.part1')}</span>
          <span className="text-4xl font-bold">{t('HeroSection.title_sentence.strong2')}</span>
          <br />
          <span className="text-4xl">{t('HeroSection.title_sentence.part2')}</span>
          <span className="text-4xl font-bold">{t('HeroSection.title_sentence.strong3')}</span>
        </p>
        <a href="#WFIArticleSection" className="scroll-smooth">
          <img
            src="/arrow_down.png"
            alt="Flèche vers le bas"
            className="mt-10 w-10 h-10 animate-bounce cursor-pointer"
          />
        </a>
      </hgroup>
    </header>
  );
}

// This function is used to generate a random color for the color dots of the letters of h1
const lettreColor = (): string => {
  const colors = ['#FFE9E9', '#FFC3C3', '#FF7B7B'];
  const randomIndex = Math.floor(Math.random() * colors.length);
  return colors[randomIndex];
};

interface colorText {
  lettre: string;
  color: string;
}

// This function adds the colored dot on the letters
function ColorText({ lettre, color }: colorText) {

  const isSpace = lettre === ' ';
  return (
    <div
      style={{ backgroundColor: isSpace ? 'transparent' : color }}
      className={[
        'inline-flex items-center justify-center h-28 md:w-14 text-5xl text-[#3C0A0A] rounded-[9999px] mx-[2px] uppercase font-mono font-extralight',
        isSpace ? '' : 'shadow-[0_10px_0px_rgb(0,0,0)]',
      ].join(' ')}
    >
      {lettre}
    </div>
  );
}
