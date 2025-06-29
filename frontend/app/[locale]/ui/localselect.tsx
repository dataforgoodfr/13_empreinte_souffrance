'use client';
import { useChangeLocale, useCurrentLocale } from '@/locales/client';

export const LocaleSelect = () => {
  const locale = useCurrentLocale();
  const changeLocale = useChangeLocale();

  const localesNames:  ('fr' |'en')[] = ['fr', 'en']

  return (
    <fieldset className="flex gap-2 bg-transparent text-[#3b0a0a]  text-sm font-medium rounded-lg  ">

      { localesNames.map((localeName) =>
      {
        return (
            <div key={localeName}>
              <input
                  type="radio"
                  id={localeName}
                  name="locale"
                  value={localeName}
                  checked={locale === localeName}
                  onChange={() => changeLocale(localeName)}
                  className="peer hidden"
              />
              <label
                  htmlFor={localeName}
                  className="select-none cursor-pointer px-2 py-2 rounded-lg hover:outline peer-checked:bg-[#ff7f7f] transition-all"

              >
                {localeName.toUpperCase()}
              </label>
            </div>
        )
      })}
    </fieldset>
  );
};
