import { getI18n } from '@/locales/server';
import Link from 'next/link';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faFacebook, faLinkedin, faXTwitter } from '@fortawesome/free-brands-svg-icons';
import Logo from './home-page/elements/logo-walfare-footprint';

export default async function Footer() {
  const t = await getI18n();

  return (
    <footer className="bg-white text-[#3b0a0a] text-sm">
      <div className="grid grid-cols-2 md:grid-cols-3 py-4 md:py-0 px-6  bg-white text-[#3b0a0a] text-sm gap-y-4">
        <div className="grid gap-3">
          <Logo />
          <div className="grid gap-2 md:px-2">
            <div className="grid grid-cols-[25px_1fr]  gap-2">
              <FontAwesomeIcon icon={faFacebook} className="text-xl" />
              <Link target="_blank" href={'https://www.facebook.com/dataforgoodfr/'}>
                Facebook
              </Link>
            </div>
            <div className="grid grid-cols-[25px_1fr]  gap-2">
              <FontAwesomeIcon icon={faXTwitter} className="text-xl" />
              <Link target="_blank" href={'https://x.com/dataforgood_fr?lang=fr'}>
                X
              </Link>
            </div>
            <div className="grid grid-cols-[25px_1fr]  gap-2">
              <FontAwesomeIcon icon={faLinkedin} className="text-xl" />
              <Link target="_blank" href={'https://www.linkedin.com/company/dataforgood/'}>
                Linkedin
              </Link>
            </div>
          </div>
        </div>

        <div className="">
          <div className="inline-flex items-center gap-2 mb-2">
            <img src="logo_data_for_good.png" alt="Logo Data For Good" className="w-10 h-10 object-contain" />
            <h4 className="font-semibold m-0 p-0 ">Data For Good</h4>
          </div>

          <div className="">
            <Link href="/terms" className="leading-none items-start">
              Mentions légales
            </Link>
            <br />
            <Link href="mailto:dataforgood@example.com" className="leading-none mt-[-10px]">
              Contactez-nous
            </Link>
          </div>
        </div>

        <div className="col-span-full mt-6 grid grid-cols-1 md:grid-cols-2 text-sm gap-2 justify-center">
          <div className="text-center md:text-left px-2">
            <p>{t('footer.all_rights_reserved')}</p>
            <p>{t('footer.rights')}</p>
          </div>
          <div className="text-center md:text-right mt-6 px-2">
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
