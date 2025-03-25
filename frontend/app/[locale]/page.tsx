import HeroSection from '@/app/[locale]/ui/general/hero-section';
import { LocaleSelect } from './ui/localselect';

export default function Home() {
  return (
    <>
      <LocaleSelect />
      <HeroSection />
    </>
  );
}
