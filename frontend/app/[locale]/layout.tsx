import '@fortawesome/fontawesome-svg-core/styles.css';
import { config } from '@fortawesome/fontawesome-svg-core';
import { I18nProviderClient } from '@/locales/client';
import { ReactElement } from 'react';
import Navbar from './ui/general/navbar';
import Footer from '@/app/[locale]/ui/general/footer';

config.autoAddCss = false;

export default async function Layout({
  params,
  children,
}: {
  params: Promise<{ locale: string }>;
  children: ReactElement;
}) {
  const { locale } = await params;

  return (
    <>
      <header className="sticky top-0 z-5">
        <div className="w-full">
          <Navbar />
        </div>
      </header>
      <I18nProviderClient locale={locale}>{children}</I18nProviderClient>
      <footer>
        <Footer />
      </footer>
    </>
  );
}
