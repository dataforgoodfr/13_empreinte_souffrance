import { getI18n } from '@/locales/server';
import Link from 'next/link';
import { faFacebook, faLinkedin, faXTwitter, faYoutube } from '@fortawesome/free-brands-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import Logo from './home-page/elements/logo-walfare-footprint';

export default async function Footer() {
  const t = await getI18n();

  return (
    <footer className="bg-white text-[#3b0a0a] text-sm p-4">
      <div className="grid grid-cols-2 md:grid-cols-3 py-4 md:py-0 px-6  bg-white text-[#3b0a0a] text-sm ">
        <div className="flex flex-col gap-3">
          <Link href="https://animafrance.org/" target="_blank" className="w-fit">
            <img src="/anima-logo.png" alt="" className="w-35 h-[35px] " />
          </Link>
          <Link
            target="_blank"
            href="https://www.youtube.com/@assoanima"
            className="inline-flex items-center gap-2 mb-0 w-fit"
          >
            <FontAwesomeIcon icon={faYoutube} style={{ width: 20, height: 20 }} />
            Youtube
          </Link>
          <Link
            target="_blank"
            href="https://www.linkedin.com/company/animafrance/"
            className="flex items-center gap-2 mb-0 w-fit"
          >
            <FontAwesomeIcon icon={faLinkedin} style={{ width: 20, height: 20 }} />
            Linkedin
          </Link>
          <Link
            target="_blank"
            href="https://animafrance.org/#contact"
            className="leading-none flex items-center gap-2 mb-0 w-fit"
          >
            {t('footer.contact_us')}
          </Link>
        </div>
        <div className="flex flex-col gap-3">
          <Link href="https://dataforgood.fr/" target="_blank" className="inline-flex items-center gap-2 w-fit">
            <img src="/logo_data_for_good.png" alt="Logo Data For Good" className="w-10 h-10 object-contain" />
            <h4 className="font-semibold m-0 p-0">Data For Good</h4>
          </Link>
          <Link
            target="_blank"
            href="https://www.facebook.com/dataforgoodfr/"
            className="flex items-center gap-2 mb-0 w-fit"
          >
            <FontAwesomeIcon icon={faFacebook} style={{ width: 20, height: 20 }} />
            Facebook
          </Link>
          <Link
            target="_blank"
            href="https://x.com/dataforgood_fr?lang=fr"
            className="flex items-center gap-2 mb-0 w-fit"
          >
            <FontAwesomeIcon icon={faXTwitter} style={{ width: 20, height: 20 }} />X
          </Link>
          <Link
            target="_blank"
            href="https://www.linkedin.com/company/dataforgood/"
            className="flex items-center gap-2 mb-0 w-fit"
          >
            <FontAwesomeIcon icon={faLinkedin} style={{ width: 20, height: 20 }} />
            Linkedin
          </Link>
          <Link href="mailto:contact@dataforgood.fr" className="leading-none flex items-center gap-2 mb-0 w-fit">
            {t('footer.contact_us')}
          </Link>
        </div>

        <div className="flex flex-col gap-2 items-center justify-center md:items-start md:justify-start col-span-full md:col-span-1 mt-10 md:mt-0">
          <Logo />
          <div className="flex flex-row items-center gap-2 md:px-2">
            <p>{t('footer.by')}</p>
            <Link href="https://animafrance.org/" target="_blank">
              <img src="/anima-logo.png" alt="" className="w-25 " />
            </Link>
          </div>
          <div className="flex flex-row items-center gap-2 md:px-2">
            <p>{t('footer.and')}</p>
            <Link href="https://dataforgood.fr/" target="_blank" className="inline-flex items-center gap-2">
              <img src="/logo_data_for_good.png" alt="Logo Data For Good" className="w-10 h-10 object-contain" />
              <h4 className="font-semibold m-0 p-0">Data For Good</h4>
            </Link>
          </div>
          <Link
            target="_blank"
            href="https://animafrance.org/je-donne"
            className="bg-[#ff7f7f] transition-all duration-200 hover:bg-[#b5abff]  text-[#3b0a0a] font-mono font-bold py-4 px-6 rounded-full shadow-[4px_4px_0_#000] text-center  w-40"
          >
            {t('footer.donate')}
          </Link>
        </div>

        <div className="col-span-full mt-6 grid grid-cols-1 md:grid-cols-2 text-sm gap-2 justify-center">
          <div className="text-center md:text-left px-2 grid grid-rows-1">
            {/* Ligne avec les deux éléments */}
            <div className="flex flex-wrap gap-2 justify-center md:justify-start items-center">
              <span>{t('footer.all_rights_reserved')}</span>
              <p>-</p>
              <Link href="/terms" className="leading-none">
                {t('footer.legal_terms')}
              </Link>
            </div>

            {/* Le reste du texte en-dessous */}
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
