'use client';
import { useChangeLocale, useCurrentLocale } from '@/locales/client';
import clsx from 'clsx';

export const LocaleSelect = () => {
  const locale = useCurrentLocale();
  const changeLocale = useChangeLocale();

  const localesNames: ('fr' | 'en')[] = ['fr', 'en'];

  return (
    <fieldset className="flex gap-2 dark-text text-sm font-medium rounded-lg">
      {localesNames.map((localeName) => (
        <label
          key={localeName}
          htmlFor={localeName}
          className={clsx(
            'relative select-none px-2 py-2 rounded-lg transition-all has-[input:focus]:outline-2 has-[input:focus]:outline-offset-2 font-bold',
            {
              'bg-pink-3': locale === localeName,
            }
          )}
        >
          <input
            type="radio"
            id={localeName}
            name="locale"
            value={localeName}
            checked={locale === localeName}
            onChange={() => changeLocale(localeName)}
            className="absolute inset-0 opacity-0 w-full h-full cursor-pointer"
          />
          {localeName.toUpperCase()}
        </label>
      ))}
    </fieldset>
  );
};
