import { getI18n } from '@/locales/server';
import Image from 'next/image';

export default async function BookAnnouncementSection() {
  const t = await getI18n();

  return (
    <section
      id="BookAnnouncementSection"
      className="min-h-screen p-8 sm:px-16 flex flex-col lg:flex-row items-center justify-center bg-[#ece6fa]"
      aria-labelledby="book-announcement-heading"
    >
      <article className="max-w-xl lg:mr-16">
        <header>
          <h2
            id="book-announcement-heading"
            className="text-4xl sm:text-5xl lg:text-6xl font-extrabold font-mono text-[#3b0a0a] mb-8"
          >
            {t('BookAnnouncement.title')}
          </h2>
        </header>
        <main>
          <p className="text-[#3b0a0a] text-base sm:text-lg mb-4">
            {t('BookAnnouncement.intro')}&nbsp;
            <strong>
              <em>{t('BookAnnouncement.bookTitle')}</em>
            </strong>
            &nbsp;{t('BookAnnouncement.publisher')}.
          </p>
          <p className="text-[#3b0a0a] text-base sm:text-lg">{t('BookAnnouncement.description')}</p>
        </main>
      </article>
      <figure className="mt-12 lg:mt-0 flex-shrink-0 relative">
        <Image
          src="/book-cover-quantifying-pain.png"
          width={340}
          height={440}
          alt={t('BookAnnouncement.imageAlt')}
          className="block rounded shadow-lg"
        />
        <figcaption className="sr-only">{t('BookAnnouncement.figcaption')}</figcaption>
        <span
          aria-hidden="true"
          className="absolute left-4 bottom-[-16px] w-[340px] h-[20px] bg-[#b39ddb] rounded blur-[2px] -z-10"
        />
      </figure>
    </section>
  );
}
