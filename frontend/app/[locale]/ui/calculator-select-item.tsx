'use client';

import { useState } from 'react';

type FarmingType = 'cage' | 'ground';
type FarmingKey = 'Option1' | 'Option2';
type QuantityKey = 'Option1' | 'Option2' | 'Option3' | 'Option4';

type Props = {
  quantities: { key: QuantityKey; label: string; factor: number }[];
  farmings: { key: FarmingKey; label: string; value: FarmingType }[];
  labels: {
    fromFarming: string;
    containsAverage: string;
    discomfort: string;
    pain: string;
    intense: string;
    agony: string;
  };
};

const sufferingData: Record<
  FarmingType,
  {
    discomfort: number;
    pain: number;
    intense: number;
    agony: number;
  }
> = {
  cage: { discomfort: 20.5, pain: 10.5, intense: 30.8, agony: 0.5 },
  ground: { discomfort: 6.92, pain: 5.8, intense: 31.2, agony: 0.5 },
};

export default function CalculatorSelect({ quantities, farmings, labels }: Props) {
  const [quantityKey, setQuantityKey] = useState<QuantityKey>('Option1');
  const [farmingKey, setFarmingKey] = useState<FarmingKey>('Option1');

  const quantity = quantities.find((q) => q.key === quantityKey)!;
  const farming = farmings.find((f) => f.key === farmingKey)!;

  const data = sufferingData[farming.value];
  const factor = quantity.factor;

  return (
    <section className="p-4 flex flex-col items-center justify-center rounded-lg text-lg space-y-4 gap-8">
      
      <div className="flex justify-center text-[#3b0a0a] font-extrabold tracking-wide lg:flex-row flex-wrap w-full gap-8">
        <select
          value={quantityKey}
          onChange={(e) => setQuantityKey(e.target.value as QuantityKey)}
          className=" border rounded text-center"
        >
          {quantities.map((q) => (
            <option key={q.key} value={q.key}>
              {q.label}
            </option>
          ))}
        </select>

        <h2>{labels.fromFarming}</h2>

        <select
          value={farmingKey}
          onChange={(e) => setFarmingKey(e.target.value as FarmingKey)}
          className=" border pr-2 pl-2 rounded text-center"
        >
          {farmings.map((f) => (
            <option key={f.key} value={f.key}>
              {f.label}
            </option>
          ))}
        </select>

        <h2>{labels.containsAverage} : </h2>
      </div>

      <div className="flex flex-col gap-5 justify-between text-[#3b0a0a] font-extrabold tracking-wide md:flex-col lg:flex-row  w-full">

        <hgroup>
          <h2 className="bg-[#ff7f7f] text-center text-3xl sm:text-6xl flex justify-start items-center w-fit">
            {(data.discomfort * factor).toFixed(1)}
          </h2>
          <h3 className="text-xl sm:text-2xl">{labels.discomfort}</h3>
        </hgroup>

        <hgroup>
          <h2 className="bg-[#ff7f7f] text-center text-3xl sm:text-6xl flex justify-start items-center w-fit">
            {(data.pain * factor).toFixed(1)}
          </h2>
          <h3 className="text-xl sm:text-2xl"> {labels.pain}</h3>
        </hgroup>

        <hgroup>
          <h2 className="bg-[#ff7f7f] text-center text-3xl sm:text-6xl flex justify-start items-center w-fit">
            {(data.intense * factor).toFixed(1)}
          </h2>
          <h3 className="text-xl sm:text-2xl">{labels.intense}</h3>
        </hgroup>

        <hgroup>
          <h2 className="bg-[#ff7f7f] text-center text-3xl sm:text-6xl flex justify-start items-center w-fit">
            {(data.agony * factor).toFixed(1)}
          </h2>
          <h3 className="text-xl sm:text-2xl">{labels.agony}.</h3>
        </hgroup>

      </div>

    </section>
  );
}
