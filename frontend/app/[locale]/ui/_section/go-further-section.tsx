import { getI18n } from '@/locales/server';
import TwitterShareButton from '@/app/actions/share-actions';
import BoltIcon from '@/app/[locale]/ui/_components/BoltIconV2';
import ButtonLink from '@/app/[locale]/ui/_components/button-link';

export default async function GoFurtherSection() {
  const t = await getI18n();

  return (
    <section id="GoFurtherSection" className="mb-10 p-8 sm:px-16 scroll-mt-18" aria-labelledby="go-further-heading">
      <div className="flex justify-center mb-6" aria-hidden="true">
        <div className="bg-brown w-16 h-28 rounded-full flex items-center justify-center">
          <BoltIcon className="text-pink-3 w-5" />
        </div>
      </div>
      <h2
        id="go-further-heading"
        className="text-3xl sm:text-4xl font-extrabold tracking-wide dark-text mb-10 text-center"
      >
        {t('GoFurther.title')}
      </h2>
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-6 max-w-4xl mx-auto">
        <ButtonLink
          href="/methodology"
          aria_label={t('GoFurther.primary')}
          button_text={t('GoFurther.primary')}
          width="full"
        />
        <ButtonLink
          href="/about"
          aria_label={t('GoFurther.aboutThisWebsite')}
          button_text={t('GoFurther.aboutThisWebsite')}
          width="full"
        />
        <TwitterShareButton nameLien={t('GoFurther.share')} shareMessage={t('twitterShare.message')} />
        <ButtonLink
          href="/kit_presse_demo.pdf"
          aria_label={t('GoFurther.downloadMediaKit')}
          button_text={t('GoFurther.downloadMediaKit')}
          background_color_name="white"
          width="full"
          download={true}
        />
      </div>
    </section>
  );
}
