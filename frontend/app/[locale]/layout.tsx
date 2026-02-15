import '@fortawesome/fontawesome-svg-core/styles.css';
import { config } from '@fortawesome/fontawesome-svg-core';
import { I18nProviderClient } from '@/locales/client';
import { ReactNode } from 'react';
import Navbar from './ui/_sections/navbar';
import Footer from '@/app/[locale]/ui/_sections/footer';

config.autoAddCss = false;

export default async function Layout({
  params,
  children,
}: {
  params: Promise<{ locale: string }>;
  children: ReactNode;
}) {
  const { locale } = await params;

  return (
    <>
      <header className="fixed top-0 z-50 w-full flex flex-row items-center justify-between">
        <Navbar />
      </header>
      <div className="pt-16">
        <I18nProviderClient locale={locale}>{children}</I18nProviderClient>
      </div>
      <footer>
        <Footer />
      </footer>
    </>
  );
}
