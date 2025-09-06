import { getI18n } from '@/locales/server';
import Link from 'next/link';
import Logo from '../_components/logo-walfare-footprint';

export default async function Footer() {
  const t = await getI18n();
  
  const footerLinkClasses = "text-[#3b0a0a]/70 hover:text-[#3b0a0a] transition-colors duration-200";

  return (
    <footer className="bg-white px-6 md:px-12 pt-8 md:pt-12 pb-8">
      <div className="max-w-7xl mx-auto flex flex-col">
        <div className="w-32 md:w-40 mx-auto md:mx-0">
          <Logo />
        </div>
        <hr className="border-[#3b0a0a] my-6 md:my-8" />
        <p className="text-sm mb-8 text-center md:text-left">{t('footer.by')}</p>
        
        {/* Grid container avec centrage */}
        <div className="w-full mb-12 md:mb-16">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-12 md:gap-72 max-w-4xl mx-auto">
            {/* Anima */}
            <section className="flex flex-col items-center md:items-start">
              <img
                src="/anima-logo.png"
                alt={t('footer.anima_logo_alt')}
                className="h-8 w-auto"
              />
              <ul className="space-y-2 mt-4 text-[13px] font-light text-center md:text-left">
                <li>
                  <Link href="https://animafrance.org/" target="_blank" className={footerLinkClasses}>Site internet</Link>
                </li>
                <li>
                  <Link href="https://www.linkedin.com/company/animafrance/" target="_blank" className={footerLinkClasses}>Linkedin</Link>
                </li>
                <li>
                  <Link href="https://www.facebook.com/animafrance.org" target="_blank" className={footerLinkClasses}>Facebook</Link>
                </li>
                <li>
                  <Link href="https://www.instagram.com/assoanima" target="_blank" className={footerLinkClasses}>Instagram</Link>
                </li>
                <li>
                  <Link href="mailto:contact@animafrance.org" target="_blank" className={footerLinkClasses}>Email</Link>
                </li>
              </ul>
            </section>
            
            {/* Data For Good */}
            <section className="flex flex-col items-center md:items-start">
              <div className="flex items-center gap-3 justify-center md:justify-start w-full">
                <img
                  src="/logo_data_for_good.png"
                  alt={t('footer.dfg_logo_alt')}
                  className="h-10 w-10 rounded-full"
                />
                <span className="text-lg font-normal">Data For Good</span>
              </div>
              <ul className="space-y-2 mt-4 text-[13px] font-light text-center md:text-left">
                <li>
                  <Link href="https://dataforgood.fr/" target="_blank" className={footerLinkClasses}>Site internet</Link>
                </li>
                <li>
                  <Link href="https://www.linkedin.com/company/dataforgood/" target="_blank" className={footerLinkClasses}>Linkedin</Link>
                </li>
                <li>
                  <Link href="mailto:contact@dataforgood.fr" target="_blank" className={footerLinkClasses}>Email</Link>
                </li>
              </ul>
            </section>
          </div>
        </div>

        {/* Footer bottom */}
        <div className="flex flex-col md:flex-row justify-between items-center md:items-start text-[11px] text-[#3b0a0a]/60 font-light">
          <div className="space-y-0.5 text-center md:text-left mb-4 md:mb-0">
            <div>Tous droits réservé - <Link href="/terms" className="underline decoration-1 underline-offset-1">Mentions Légales</Link></div>
            <div>© 2025 Empreinte Souffrance et Data for Good</div>
          </div>
          <div className="text-center md:text-right">
            Graphisme : <Link href="https://coucou.design" target="_blank" className="underline decoration-1 underline-offset-1">Coucou.Design</Link>
          </div>
        </div>
      </div>
    </footer>
  );
}
