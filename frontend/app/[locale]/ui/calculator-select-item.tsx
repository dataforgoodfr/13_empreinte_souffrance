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
  cage: { discomfort: 2.5, pain: 1.2, intense: 0.7, agony: 30 },
  ground: { discomfort: 1.5, pain: 0.8, intense: 0.4, agony: 20 },
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
          className=" border pr-2 pl-2 rounded txt-center"
        >
          {farmings.map((f) => (
            <option key={f.key} value={f.key}>
              {f.label}
            </option>
          ))}
        </select>

        <h2>{labels.containsAverage} : </h2>
      </div>

      <div className="flex flex-row justify-between text-[#3b0a0a] font-extrabold tracking-wide lg:flex-row flex-wrap w-full">

        <hgroup>
          <h2 className="bg-[#ff7f7f] text-center text-3xl sm:text-6xl flex justify-start items-center w-fit">
            {Math.ceil(data.discomfort * factor)}
          </h2>
          <h3 className="text-xl sm:text-2xl">{labels.discomfort}</h3>
        </hgroup>

        <hgroup>
          <h2 className="bg-[#ff7f7f] text-center text-3xl sm:text-6xl flex justify-start items-center w-fit">
            {Math.ceil(data.pain * factor)}
          </h2>
          <h3 className="text-xl sm:text-2xl"> {labels.pain}</h3>
        </hgroup>

        <hgroup>
          <h2 className="bg-[#ff7f7f] text-center text-3xl sm:text-6xl flex justify-start items-center w-fit">
            {Math.ceil(data.intense * factor)}
          </h2>
          <h3 className="text-xl sm:text-2xl">{labels.intense}</h3>
        </hgroup>

        <hgroup>
          <h2 className="bg-[#ff7f7f] text-center text-3xl sm:text-6xl flex justify-start items-center w-fit">
            {Math.ceil(data.agony * factor)}
          </h2>
          <h3 className="text-xl sm:text-2xl">{labels.agony}.</h3>
        </hgroup>

      </div>

    </section>
  );
}
