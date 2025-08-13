import { useParams } from 'next/navigation';

export default (): string => {
  const { locale } = useParams();

  if (typeof locale === 'string') {
    return `/${locale}`;
  }

  if (Array.isArray(locale)) {
    return `/${locale[0]}`;
  }

  return '';
};
