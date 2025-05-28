import { getI18n } from '@/locales/server';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faBolt } from '@fortawesome/free-solid-svg-icons';
import Link from 'next/link';

export default async function GoFurtherSection() {
    const t = await getI18n();

    return (
        <section
            className="bg-white min-h-screen p-8 sm:px-16"
            aria-labelledby="go-further-heading"
        >
            <div className="flex justify-center mb-6" aria-hidden="true">
                <div className="bg-indigo-300 w-14 h-20 rounded-full flex items-center justify-center shadow-[4px_4px_0_#000]">
                  <span className="rotate-[-18deg] text-[40px] text-black">
                    <FontAwesomeIcon icon={faBolt} />
                  </span>
                </div>
            </div>

            <h2
                id="go-further-heading"
                className="text-3xl sm:text-4xl font-extrabold tracking-wide text-[#3b0a0a] mb-10 text-center"
            >
                {t('GoFurther.title')}
            </h2>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-6 max-w-3xl mx-auto">
                <form action="/download-kit" method="post">
                    <button
                        type="submit"
                        className="w-full bg-[#ff7f7f] text-[#3b0a0a] font-mono font-bold py-4 px-6 rounded-full shadow-[4px_4px_0_#000] cursor-pointer"
                        aria-label={t('GoFurther.downloadMediaKit')}
                    >
                        {t('GoFurther.downloadMediaKit')}
                    </button>
                </form>

                <form action="/share" method="post">
                    <button
                        type="submit"
                        className="w-full bg-[#ff7f7f] text-[#3b0a0a] font-mono font-bold py-4 px-6 rounded-full shadow-[4px_4px_0_#000] cursor-pointer"
                        aria-label={t('GoFurther.share')}
                    >
                        {t('GoFurther.share')}
                    </button>
                </form>

                <form action="/methodology" method="post">
                    <button
                        type="submit"
                        className="w-full bg-[#ff7f7f] text-[#3b0a0a] font-mono font-bold py-4 px-6 rounded-full shadow-[4px_4px_0_#000] cursor-pointer"
                        aria-label={t('GoFurther.methodology')}
                    >
                        {t('GoFurther.methodology')}
                    </button>
                </form>

                <Link
                    href="/about"
                    className="w-full text-center bg-[#ff7f7f] text-[#3b0a0a] font-mono font-bold py-4 px-6 rounded-full shadow-[4px_4px_0_#000] flex items-center justify-center"
                    aria-label={t('GoFurther.aboutThisWebsite')}
                >
                    {t('GoFurther.aboutThisWebsite')}
                </Link>
            </div>
        </section>
    );
}
