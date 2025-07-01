import { getScopedI18n } from '@/locales/server';
import CalculatorSelect from "@/app/[locale]/ui/calculator-select-item";

export default async function SelectorSection() {
  const scopedT = await getScopedI18n("calculatorPage");

  const quantities = [
    { key: 'Option4', label: scopedT('calculSection.selectorSection.selector1.Option4'), factor: 1 },
    { key: 'Option1', label: scopedT('calculSection.selectorSection.selector1.Option1'), factor: 2 },
    { key: 'Option2', label: scopedT('calculSection.selectorSection.selector1.Option2'), factor: 6 },
    { key: 'Option3', label: scopedT('calculSection.selectorSection.selector1.Option3'), factor: 12 },
  ] as const;

  const farmings = [
    { key: 'Option1', label: scopedT('calculSection.selectorSection.selector2.Option1'), value: 'cage' },
    { key: 'Option2', label: scopedT('calculSection.selectorSection.selector2.Option2'), value: 'ground' },
  ] as const;

  const labels = {
    fromFarming: scopedT('calculSection.selectorSection.texte1'),
    containsAverage: scopedT('calculSection.selectorSection.selector2.texte2'),
    discomfort: scopedT('calculSection.keySection.key1'),
    pain: scopedT('calculSection.keySection.key2'),
    intense: scopedT('calculSection.keySection.key3'),
    agony: scopedT('calculSection.keySection.key4'),
  };

  return (
    <section className=" bg-white scroll-mt-18 max-w-screen p-8 sm:px-16 w-full flex flex-col gap-16">
      <CalculatorSelect quantities={[...quantities]} farmings={[...farmings]} labels={labels} />
    </section>
  );
}
