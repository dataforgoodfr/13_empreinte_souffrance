import { getI18n } from '@/locales/server';
import Link from 'next/link';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faFacebook, faLinkedin, faXTwitter } from '@fortawesome/free-brands-svg-icons';
import BtnImprintSuffering from './home-page/elements/btn-imprint-suffering';

export default async function Footer() {
  const t = await getI18n();

  return (
    <footer className="bg-white text-[#3b0a0a] text-sm">
      <div className="grid grid-cols-2 md:grid-cols-3 gap-8 px-6 py-8 bg-white text-[#3b0a0a] text-sm gap-y-4">
        <div className="grid gap-3">
          <BtnImprintSuffering />
          <div className="grid gap-2">
            <div className="grid grid-cols-[25px_1fr] items-center gap-2">
              <FontAwesomeIcon icon={faFacebook} className="text-xl" />
              <Link target="_blank" href={'https://www.facebook.com/dataforgoodfr/'}>
                Facebook
              </Link>
            </div>
            <div className="grid grid-cols-[25px_1fr] items-center gap-2">
              <FontAwesomeIcon icon={faXTwitter} className="text-xl" />
              <Link target="_blank" href={'https://x.com/dataforgood_fr?lang=fr'}>
                X
              </Link>
            </div>
            <div className="grid grid-cols-[25px_1fr] items-center gap-2">
              <FontAwesomeIcon icon={faLinkedin} className="text-xl" />
              <Link target="_blank" href={'https://www.linkedin.com/company/dataforgood/'}>
                Linkedin
              </Link>
            </div>
          </div>
        </div>

        <div className="grid gap-3">
          <div className="grid grid-cols-[40px_1fr] items-center gap-3">
            <img src="logo_data_for_good.png" alt="Logo Data For Good" className="w-10 h-10 object-contain" />
            <h4 className="font-semibold">Data For Good</h4>
          </div>

          {/* todo! create page with link or delete link ? */}
          <Link href="/terms">{t('footer.legal_terms')}</Link>
          <Link href="/privacy-policy">{t('footer.privacy_policy')}</Link>
          <Link href="/contact">{t('footer.contact_us')}</Link>
        </div>

        <div className="col-span-full mt-6 grid grid-cols-1 md:grid-cols-2 text-sm gap-2">
          <div className="text-center md:text-left">
            <p>{t('footer.all_rights_reserved')}</p>
            <p>{t('footer.rights')}</p>
          </div>
          <div className="text-center md:text-right">
            <p>
              {t('footer.graphics')}{' '}
              <Link href="https://coucou.design" target="_blank" className="underline">
                Coucou.Design
              </Link>
            </p>
          </div>
        </div>
      </div>
    </footer>
  );
}
