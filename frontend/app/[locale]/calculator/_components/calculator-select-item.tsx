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
    <section className="p-section flex flex-col items-center justify-center gap-16">

      <div className="flex flex-col md:flex-row items-center justify-center text-brown text-bold gap-8">
        <select
          value={quantityKey}
          onChange={(e) => setQuantityKey(e.target.value as QuantityKey)}
          className="bg-pink-1 shadow-[0_5px_0px_black] rounded-[10px] text-center px-6 py-2"
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
          className="bg-pink-1 shadow-[0_5px_0px_black] rounded-[10px] text-center px-6 py-2"
        >
          {farmings.map((f) => (
            <option key={f.key} value={f.key}>
              {f.label}
            </option>
          ))}
        </select>

        <h2>{labels.containsAverage} : </h2>
      </div>

      <div className="flex flex-col md:flex-row justify-between text-brown font-extrabold tracking-wide  gap-5 w-full">

        <hgroup>
          <span className="bg-pink-1 text-center text-numbers flex justify-start items-center w-fit rounded-[5px]">
            {Math.round(data.discomfort * factor)}
          </span>
          <h3 className="text-xl sm:text-2xl">{labels.discomfort}</h3>
        </hgroup>

        <hgroup>
          <span className="bg-pink-2 text-center text-numbers flex justify-start items-center w-fit rounded-[5px]">
            {Math.round(data.pain * factor)}
          </span>
          <h3 className="text-xl sm:text-2xl"> {labels.pain}</h3>
        </hgroup>

        <hgroup>
          <span className="bg-pink-3 text-center text-numbers flex justify-start items-center w-fit rounded-[5px]">
            {Math.round(data.intense * factor)}
          </span>
          <h3 className="text-xl sm:text-2xl">{labels.intense}</h3>
        </hgroup>

        <hgroup>
          <span className="bg-brown text-pink-1 text-center text-numbers flex justify-start items-center w-fit rounded-[5px]">
            {Math.round(data.agony * factor)}
          </span>
          <h3 className="text-xl sm:text-2xl">{labels.agony}.</h3>
        </hgroup>

      </div>

    </section>
  );
}
