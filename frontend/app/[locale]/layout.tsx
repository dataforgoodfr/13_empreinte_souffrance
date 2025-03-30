import { I18nProviderClient } from '@/locales/client';
import { ReactElement } from 'react';
import Navbar from './ui/general/navbar';

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
      <header>
        <div className="w-full flex-none fixed">
          <Navbar />
        </div>
      </header>
      <I18nProviderClient locale={locale}>{children}</I18nProviderClient>
    </>
  );
}
