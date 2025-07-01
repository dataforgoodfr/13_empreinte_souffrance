'use client';
import { useChangeLocale, useCurrentLocale } from '@/locales/client';

export const LocaleSelect = () => {
  const locale = useCurrentLocale();
  const changeLocale = useChangeLocale();

  const localesNames: ('fr' | 'en')[] = ['fr', 'en'];

  return (
    <fieldset className="flex gap-2 bg-transparent text-[#3b0a0a] text-sm font-medium rounded-lg">
      {localesNames.map((localeName) => (
        <label
          key={localeName}
          htmlFor={localeName}
          className="relative cursor-pointer select-none px-2 py-2 rounded-lg transition-all
                     has-[input:focus]:outline has-[input:focus]:outline-2 has-[input:focus]:outline-offset-2
                     has-[input:checked]:bg-[#ff7f7f]"
        >
          <input
            type="radio"
            id={localeName}
            name="locale"
            value={localeName}
            checked={locale === localeName}
            onChange={() => changeLocale(localeName)}
            className="absolute inset-0 opacity-0 w-full h-full"
          />
          {localeName.toUpperCase()}
        </label>
      ))}
    </fieldset>
  );
};
