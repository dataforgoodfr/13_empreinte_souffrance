import { getI18n } from '@/locales/server';
import Link from 'next/link';
import TwitterShareButton from '@/app/actions/share-actions';
import BoltIcon from "@/app/[locale]/ui/icons/BoltIcon";

export default async function GoFurtherSection() {
  const t = await getI18n();

  return (
    <section id="GoFurtherSection" className="mb-10 p-8 sm:px-16 scroll-mt-18" aria-labelledby="go-further-heading">
      <div className="flex justify-center mb-6" aria-hidden="true">
        <div className="bg-violet-2 w-14 h-20 rounded-full flex items-center justify-center shadow-[4px_4px_0_#000]">
          <BoltIcon color='black'/>
        </div>
      </div>
      <h2
        id="go-further-heading"
        className="text-3xl sm:text-4xl font-extrabold tracking-wide dark-text mb-10 text-center"
      >
        {t('GoFurther.title')}
      </h2>
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-6 max-w-3xl mx-auto">
        <form>
          {/* <form action={downloadMediaKit}> */}
          {/* <button
            type="submit"
            className="w-full bg-(--pink-3) dark-text font-mono font-bold py-4 px-6 rounded-full shadow-[4px_4px_0_#000] cursor-pointer transition-all duration-200 hover:bg-(--violet-1)"
            aria-label={t('GoFurther.downloadMediaKit')}
          >
            {t('GoFurther.downloadMediaKit')}
          </button> */}
          <a
            href="/kit_presse_demo.pdf"
            download
            className="w-full text-center dark-text font-mono font-bold py-4 px-6 rounded-full shadow-[4px_4px_0_#000] flex items-center justify-center transition-all duration-200 bg-(--pink-3) hover:bg-(--violet-1)"
            aria-label={t('GoFurther.downloadMediaKit')}
          >
            {t('GoFurther.downloadMediaKit')}
          </a>
        </form>
        <TwitterShareButton nameLien={t('GoFurther.share')} />
        <Link
          href="/methodology"
          className="w-full text-center  dark-text font-mono font-bold py-4 px-6 rounded-full shadow-[4px_4px_0_#000] flex items-center justify-center transition-all duration-200 bg-(--pink-3) hover:bg-(--violet-1)"
          aria-label={t('GoFurther.methodology')}
        >
          {t('GoFurther.methodology')}
        </Link>

        <Link
          href="/about"
          className="w-full text-center  dark-text font-mono font-bold py-4 px-6 rounded-full shadow-[4px_4px_0_#000] flex items-center justify-center transition-all duration-200 bg-(--pink-3) hover:bg-(--violet-1) "
          aria-label={t('GoFurther.aboutThisWebsite')}
        >
          {t('GoFurther.aboutThisWebsite')}
        </Link>
      </div>
    </section>
  );
}
