import ResultsSection from '@/app/[locale]/home/_sections/results-section';
import GoFurtherSection from '@/app/[locale]/ui/_sections/go-further-section';
import ProgressSection from './home/_sections/progress-section';
import HeroPressSection from './home/_sections/hero-press-section';
import PromiseKeptSection from './home/_sections/promise-kept-section';

export default function Home() {
  return (
    <>
      <HeroPressSection />
      <PromiseKeptSection />
      <ProgressSection />
      <ResultsSection />
      <GoFurtherSection />
    </>
  );
}
