'use client';
import { useChangeLocale, useCurrentLocale } from '@/locales/client';

export const LocaleSelect = () => {
  const locale = useCurrentLocale();
  const changeLocale = useChangeLocale();

  return (
    <select
      className="bg-green-300 text-gray-800 px-2 md:px-6 py-3 text-lg font-medium rounded-lg shadow-lg hover:bg-green-400"
      value={locale}
      onChange={(e) => changeLocale(e.target.value as 'fr' | 'en')}
    >
      <option value="en">English</option>
      <option value="fr">Français</option>
    </select>
  );
};
