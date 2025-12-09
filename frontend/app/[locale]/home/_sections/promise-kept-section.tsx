import { getI18n } from '@/locales/server';
import SectionTitle from '../_components/section-title';
import ArrowDown from '../../ui/_logo/ArrowDown';

export default async function PromiseKeptSection() {
  const t = await getI18n();

  return (
    <section
      id="PromiseKeptSection"
      className="relative p-section flex flex-col items-center justify-center bg-black text-center h-full"
      aria-labelledby="go-further-heading"
    >
      <div className="h-svh max-w-contain flex items-center justify-center mb-20">
        <SectionTitle
          image_path="hollow_egg.svg"
          image_alt=""
          title={
            <>
              {t('PromiseKept.promiseKept').toUpperCase()} <br />
              {t('PromiseKept.timeToReckon').toUpperCase()}.
            </>
          }
          text_color="white"
        />
      </div>
      <span className="absolute bottom-0 animate-bounce">
        <ArrowDown href="#ProgressSection" />
      </span>
    </section>
  );
}
