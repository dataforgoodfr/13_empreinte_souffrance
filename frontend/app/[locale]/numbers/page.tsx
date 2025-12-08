import GoFurtherSection from '../ui/_sections/go-further-section';
import CagedEggsGraphSection from './_sections/caged-eggs-graph-section';
import CagedEggsMapSection from './_sections/caged-eggs-map-section';
import CommitmentSection from './_sections/commitment-section';

export default async function NumbersPage() {
  return (
    <section className="flex flex-col">
      <h1>Cette page est cours de construction </h1>
      <CommitmentSection />
      <CagedEggsGraphSection />
      <CagedEggsMapSection />
      <GoFurtherSection/>
    </section>
  );
}
