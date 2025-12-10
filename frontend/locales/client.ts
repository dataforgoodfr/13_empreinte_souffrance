'use client';
import { createI18nClient } from 'next-international/client';

export const { useI18n, useScopedI18n, I18nProviderClient, useCurrentLocale, useChangeLocale } = createI18nClient({
  fr: () => import('./fr'),
  // en: () => import('./en'),
});
