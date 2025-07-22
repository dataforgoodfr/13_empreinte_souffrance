import HeroSection from '@/app/[locale]/home/_section/hero-section';
import WFISection from '@/app/[locale]/home/_section/WFI-article-section';
import SufferingCausesSection from '@/app/[locale]/ui/_section/suffering-causes-section';
import PainEquationSection from '@/app/[locale]/home/_section/pain-equation-section';
import ResultsSection from '@/app/[locale]/home/_section/results-section';
import BookAnnouncementSection from '@/app/[locale]/home/_section/book-announcement-section';
import GoFurtherSection from '@/app/[locale]/ui/_section/go-further-section';
import LinkSection from '@/app/[locale]/ui/_section/link-section';

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
