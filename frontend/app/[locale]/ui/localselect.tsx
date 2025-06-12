'use client';
import { useChangeLocale, useCurrentLocale } from '@/locales/client';

export const LocaleSelect = () => {
  const locale = useCurrentLocale();
  const changeLocale = useChangeLocale();

  return (
    <fieldset className="flex gap-2 bg-transparent text-[#3b0a0a]  text-sm font-medium rounded-lg  ">

      <div>
        <input
          type="radio"
          id="fr"
          name="locale"
          value="fr"
          checked={locale === 'fr'}
          onChange={() => changeLocale('fr')}
          className="peer hidden"
        />
        <label
          htmlFor="fr"
          className="select-none cursor-pointer px-2 py-2 rounded-lg hover:outline peer-checked:bg-[#ff7f7f] transition-all"
        
        >
          FR
        </label>
      </div>

      <div>
        <input
          type="radio"
          id="en"
          name="locale"
          value="en"
          checked={locale === 'en'}
          onChange={() => changeLocale('en')}
          className="peer hidden"
        />
        <label
          htmlFor="en"
          className="select-none cursor-pointer px-2 py-2 rounded-lg hover:outline peer-checked:bg-[#ff7f7f] transition-all"
        >
          EN
        </label>
      </div>


    </fieldset>
  );
};