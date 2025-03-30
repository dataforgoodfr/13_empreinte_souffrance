import { getI18n } from '@/locales/server';
import Link from 'next/link';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faFacebook, faLinkedin, faXTwitter } from '@fortawesome/free-brands-svg-icons';

export default async function Footer() {
  const t = await getI18n();

  return (
    <div className="w-full flex flex-col items-center justify-around py-6 gap-3">
      <span className="text-3xl">{t('suffering_footprint').toUpperCase()}</span>
      <div className="w-full flex justify-center gap-3">
        <span>
          <FontAwesomeIcon style={{ fontSize: '25px' }} icon={faFacebook}></FontAwesomeIcon>
        </span>
        <span>
          <FontAwesomeIcon style={{ fontSize: '25px' }} icon={faXTwitter}></FontAwesomeIcon>
        </span>
        <span>
          <FontAwesomeIcon style={{ fontSize: '25px' }} icon={faLinkedin}></FontAwesomeIcon>
        </span>
      </div>
      <div className="flex gap-5">
        <Link href="/terms">{t('footer.legal_terms')}</Link>
        <Link href="/privacy-policy">{t('footer.privacy_policy')}</Link>
        <Link href="/contact">{t('footer.contact_us')}</Link>
      </div>
    </div>
  );
}
