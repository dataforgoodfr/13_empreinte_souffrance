import HeroSection from '@/app/[locale]/ui/general/home-page/hero-section';
import WFISection from '@/app/[locale]/ui/general/home-page/WFI-article-section';
import SufferingCausesSection from '@/app/[locale]/ui/general/home-page/suffering-causes-section';
import PainEquationSection from '@/app/[locale]/ui/general/home-page/pain-equation-section';
import ResultsSection from '@/app/[locale]/ui/general/home-page/results-section';
import BookAnnouncementSection from '@/app/[locale]/ui/general/home-page/book-announcement-section';
import GoFurtherSection from '@/app/[locale]/ui/general/home-page/go-further-section';
import LinkSection from '@/app/[locale]/ui/general/home-page/link-section';

export default function Home() {
  return (
    <>
      <HeroSection />
      <LinkSection />
      <WFISection />
      <SufferingCausesSection />
      <PainEquationSection />
      <ResultsSection />
      <BookAnnouncementSection />
      <GoFurtherSection />
    </>
  );
}
