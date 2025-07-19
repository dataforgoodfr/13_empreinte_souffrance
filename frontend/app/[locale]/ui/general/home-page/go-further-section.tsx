import { getI18n } from '@/locales/server';
import TwitterShareButton from '@/app/actions/share-actions';
import BoltIcon from "@/app/[locale]/ui/icons/BoltIcon";
import ButtonLink from "@/app/[locale]/ui/general/elements/button-link";

export default async function GoFurtherSection() {
    const t = await getI18n();

    return (
        <section id="GoFurtherSection" className="mb-10 p-8 sm:px-16 scroll-mt-18" aria-labelledby="go-further-heading">
            <div className="flex justify-center mb-6" aria-hidden="true">
                <div
                    className="bg-violet-2 w-14 h-20 rounded-full flex items-center justify-center shadow-[4px_4px_0_#000]">
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
                <ButtonLink
                    href="/kit_presse_demo.pdf"
                    aria_label={t('GoFurther.downloadMediaKit')}
                    button_text={t('GoFurther.downloadMediaKit')}
                    download={true}
                />
                <TwitterShareButton nameLien={t('GoFurther.share')}/>
                <ButtonLink
                    href="/methodology"
                    aria_label={t('GoFurther.methodology')}
                    button_text={t('GoFurther.methodology')}
                />
                <ButtonLink
                    href='/about'
                    aria_label={t('GoFurther.aboutThisWebsite')}
                    button_text={t('GoFurther.aboutThisWebsite')}
                />
            </div>
        </section>
    );
}
