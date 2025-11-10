import ThankingSection from './_sections/thanking_section';
import WhyNameSection from './_sections/why_name_section';
import AssociationPresentationSection from './_sections/association-presentation-section';
import GoFurtherSection from '../ui/_sections/go-further-section';
import SourcesSection from './_sections/sources_section';

export default async function About() {
  return (
    <>
      <AssociationPresentationSection />
      <WhyNameSection />
      <ThankingSection />
      <SourcesSection/>
      <GoFurtherSection/>
    </>
  );
}
