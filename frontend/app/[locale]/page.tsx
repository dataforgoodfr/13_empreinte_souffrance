import HeroSection from '@/app/[locale]/ui/general/home-page/hero-section';
import { LocaleSelect } from './ui/localselect';
import WFISection from '@/app/[locale]/ui/general/home-page/WFI-section';
import SufferingCausesSection from '@/app/[locale]/ui/general/home-page/suffering-causes-section';
import PainEquationSection from '@/app/[locale]/ui/general/home-page/pain-equation-section';
import ResultsSection from '@/app/[locale]/ui/general/home-page/results-section';
import HumanFoodSection from '@/app/[locale]/ui/general/home-page/human-food-section';
import CallToActionSection from '@/app/[locale]/ui/general/home-page/call-to-action-section';
import BookAnnouncementSection from '@/app/[locale]/ui/general/home-page/book-announcement-section';
import MethodologySection from '@/app/[locale]/ui/general/home-page/methodology-section';
import GoFurtherSection from '@/app/[locale]/ui/general/home-page/go-further-section';
import LinkSection from '@/app/[locale]/ui/general/home-page/link-section';

export default function Home() {
  return (
    <>
      <LocaleSelect />
      <HeroSection />
      <LinkSection />
      <WFISection />
      <SufferingCausesSection />
      <PainEquationSection />
      <ResultsSection />
      <HumanFoodSection />
      <MethodologySection />
      <CallToActionSection />
      <GoFurtherSection />
      <BookAnnouncementSection />
    </>
  );
}
