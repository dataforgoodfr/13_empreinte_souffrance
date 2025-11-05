import WFISection from '@/app/[locale]/home/_sections/WFI-article-section';
import SufferingCausesSection from '@/app/[locale]/ui/_sections/suffering-causes-section';
import PainEquationSection from '@/app/[locale]/home/_sections/pain-equation-section';
import ResultsSection from '@/app/[locale]/home/_sections/results-section';
import BookAnnouncementSection from '@/app/[locale]/home/_sections/book-announcement-section';
import GoFurtherSection from '@/app/[locale]/ui/_sections/go-further-section';
import LinkSection from '@/app/[locale]/ui/_sections/link-section';
import ProgressSection from './home/_sections/progress-section';
import HeroPressSection from './home/_sections/hero-press-section';

export default function Home() {
  return (
    <>
      <HeroPressSection />
      <ProgressSection />
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
