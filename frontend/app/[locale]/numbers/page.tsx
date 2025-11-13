import CagedEggsGraphSection from './_sections/caged-eggs-graph-section';
import CagedEggsMapSection from './_sections/caged-eggs-map-section';
import CommitmentSection from './_sections/commitment-section';

export default async function NumbersPage() {
  return (
    <section className="flex flex-col justify-center p-20 gap-4">
      <h1>Cette page est cours de construction </h1>
      <CommitmentSection />
      <CagedEggsGraphSection />
      <CagedEggsMapSection />
    </section>
  );
}
