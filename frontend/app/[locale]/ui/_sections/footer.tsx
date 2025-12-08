import { getI18n } from '@/locales/server';
import Link from 'next/link';
import LogoWelfare from '../_components/logo-walfare-footprint';
import ButtonLink from '@/app/[locale]/ui/_components/button-link';

export default async function Footer() {
  const t = await getI18n();

  const footerLinkClasses = 'text-brown hover:text-pink-3 transition-colors duration-200';
  const footerUnderlineClasses = `${footerLinkClasses} underline`;

  return (
    <footer className="bg-white px-6 md:px-12 py-8">
      <div className="max-w-7xl mx-auto">
        {/* Logo + Bouton Don */}
        <div className="flex">
          <div className="w-48 flex flex-col space-y-3">
            <LogoWelfare />
            <ButtonLink
              href="https://animafrance.org/je-donne"
              aria_label={t('footer.donate')}
              button_text={t('footer.donate')}
              width="small"
              open_in_new_tab={true}
            />
          </div>
        </div>

        <hr className="border-brown/20 my-8" />

        {/* Section Partenaires */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="text-sm text-brown">{t('footer.by')}</div>

          {/* Anima */}
          <div className="flex flex-col">
            <div>
              <img src="/anima-logo.svg" alt={t('footer.anima_logo_alt')} className="w-[120px] h-[28px] mb-4" />
              <ul className="space-y-3 text-sm">
                <li>
                  <a className={footerLinkClasses} href="https://animafrance.org/">
                    {t('footer.website')}
                  </a>
                </li>
                <li>
                  <a className={footerLinkClasses} href="https://www.linkedin.com/company/animafrance/">
                    {t('footer.linkedin')}
                  </a>
                </li>
                <li>
                  <a className={footerLinkClasses} href="https://www.facebook.com/animafrance.org">
                    {t('footer.facebook')}
                  </a>
                </li>
                <li>
                  <a className={footerLinkClasses} href="https://www.instagram.com/assoanima">
                    {t('footer.instagram')}
                  </a>
                </li>
                <li>
                  <a className={footerLinkClasses} href="mailto:www@animafrance.org">
                    {t('footer.email')}
                  </a>
                </li>
              </ul>
            </div>
          </div>

          {/* Data For Good */}
          <div className="flex flex-col">
            <div>
              <div className="flex items-center gap-4 mb-4">
                <img src="/logo_data_for_good.png" alt={t('footer.dfg_logo_alt')} className="h-12 w-12 rounded-full" />
                <span className="text-lg font-extrabold text-brown">Data For Good</span>
              </div>
              <ul className="space-y-3 text-sm">
                <li>
                  <a className={footerLinkClasses} href="https://dataforgood.fr/">
                    {t('footer.website')}
                  </a>
                </li>
                <li>
                  <a className={footerLinkClasses} href="https://www.linkedin.com/company/dataforgood/">
                    {t('footer.linkedin')}
                  </a>
                </li>
                <li>
                  <a className={footerLinkClasses} href="mailto:hellodataforgood@gmail.com">
                    {t('footer.email')}
                  </a>
                </li>
              </ul>
            </div>
          </div>
        </div>

        {/* Footer Bottom */}
        <div className="flex flex-col md:flex-row justify-between mt-12 text-sm text-brown">
          <div className="mb-6">
            <div>
              {t('footer.all_rights_reserved')} &nbsp;-&nbsp;
              <Link className={footerUnderlineClasses} href="/legal-notice">
                {t('footer.legal_terms')}
              </Link>
            </div>
            <div className="mt-2">{t('footer.rights')}</div>
          </div>

          <div className="md:mt-7">
            <span>{t('footer.graphics')} </span>
            <a
              className={footerUnderlineClasses}
              href="https://coucou.design"
              target="_blank"
              rel="noopener noreferrer"
            >
              Coucou.Design
            </a>
          </div>
        </div>
      </div>
    </footer>
  );
}
