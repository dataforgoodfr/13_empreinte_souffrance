import ThankingSection from './_section/thanking_section';
import WhyNameSection from './_section/why_name_section';
import AssociationPresentationSection from './_section/association-presentation-section';

export default async function About() {
  return (
    <>
      <ThankingSection />
      <WhyNameSection />
      <AssociationPresentationSection />
    </>
  );
}
