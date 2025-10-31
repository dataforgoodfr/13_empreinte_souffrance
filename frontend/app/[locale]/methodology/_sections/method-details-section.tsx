import { getI18n } from '@/locales/server';
import SectionHeading from '../../ui/_sections/section-heading';
import IdentifyPainSources from '../_components/identify-pain-sources';
import QuantifyPainBySources from '../_components/quantify-pain-by-sources';
import ComputePainSources from '../_components/compute-pain-sources';
import ListOfAffliction from '../_components/list-of-affition';

export default async function MethodDetailsSection() {
  const t = await getI18n();

  return (
    <section className="p-section bg-pink-1">
      <SectionHeading title={t('MethodologyPage.method_details_section.title_h1')} heading_number="2" />

      <div className="flex flex-col items-center mt-15 gap-16">
        <IdentifyPainSources />
        <QuantifyPainBySources />
        <ComputePainSources/>
      </div>
    </section>

  );
}
