import { getI18n } from '@/locales/server';
import clsx from 'clsx';

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
            {title.split('').map((letter: string, index: number) => (
              <ColoredText key={index} letter={letter} />
            ))}
          </span>
          <span className="inline-flex items-center justify-center h-28 md:w-14 text-5xl dark-text rounded-[9999px] mx-[2px] uppercase font-mono font-extralight shadow-[0_10px_0px_rgb(0,0,0)] bg-violet-2">
            ?
          </span>
        </h1>
        <p className="mt-4 light-text uppercase">
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

interface coloredTextType {
  letter: string;
}

function ColoredText({ letter }: coloredTextType) {
  const isSpace = letter === ' ';
  let letter_background_color = isSpace ? 'bg-transparent' : 'bg-pink-' + Math.floor(1 + Math.random() * 3);

  return (
    <div
      className={clsx(
        'inline-flex items-center justify-center h-28 md:w-14 text-5xl dark-text rounded-[9999px] mx-[2px] uppercase font-mono font-extralight',
        letter_background_color,
        {
          'shadow-[0_10px_0px_rgb(0,0,0)]': !isSpace,
        }
      )}
    >
      {letter}
    </div>
  );
}
