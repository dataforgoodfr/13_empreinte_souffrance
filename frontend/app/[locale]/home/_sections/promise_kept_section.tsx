import { getI18n } from '@/locales/server';
import Link from '../../ui/_components/Link';
import ArrowDown from '../../ui/_logo/ArrowDown';

export default async function PromiseKeptSection() {
  const t = await getI18n();

  return (
    <section
      id="PromiseKeptSection"
      className="p-section h-[90dvh] flex flex-col items-center justify-center bg-black relative"
      aria-labelledby="promise-kept-heading"
    >
    
        <img src="/empty_egg.svg" className="w-[150px]" />
        <h2 id="promise-kept-heading" className="text-h2 text-center md:text-h2-desktop font-extrabold text-grey max-w-[605px]">
          {t('PromiseKeptSection.promise_kept_question')}<br/>
          {t('PromiseKeptSection.time_for_reckoning')}
        </h2>

      <div className="flex flex-col items-center absolute bottom-0">
        <Link href={'#ProgressSection'}>
          <ArrowDown />
        </Link>
      </div>

    </section>
  );
}
