'use client';
import { useEffect, useRef, useState } from 'react';

export type Affliction = {
  title: string;
  percent: string;
  text: string;
  agony: string;
  pain: string;
  suffering: string;
  discomfort: string;
};

interface AnimatedCardProps {
  afflictions: Affliction[];
  delay?: number;
  startIndex?: number;
}

export function AnimatedCard({ afflictions, startIndex = 0, delay = 3000 }: AnimatedCardProps) {
  const [current, setCurrent] = useState(startIndex);
  const [prev, setPrev] = useState<number | null>(null);
  const timeoutRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  useEffect(() => {
    const interval = setInterval(() => {
      setPrev(current);
      setCurrent((prev) => (prev + 1) % afflictions.length);

      timeoutRef.current = setTimeout(() => setPrev(null), 400);
    }, delay);

    return () => {
      clearInterval(interval);
      if (timeoutRef.current) clearTimeout(timeoutRef.current);
    };
  }, [afflictions.length, current, delay]);

  const newCard = (
    <div
      key={current}
      className="absolute left-0 top-0 w-full transition-transform duration-400 translate-x-0"
      style={{ transform: 'translateX(+100%)' }}
    >
      <SynteseSurffering {...afflictions[current]} />
    </div>
  );

  const prevCard =
    prev !== null ? (
      <div key={prev} className="absolute left-0 top-0 w-full transition-transform duration-400">
        <SynteseSurffering {...afflictions[prev]} />
      </div>
    ) : null;

  return (
    <div className="relative w-full min-h-[150px] overflow-hidden">
      {prevCard}
      {newCard}
    </div>
  );
}

// Composant inchangé
function SynteseSurffering({ title, percent, text, agony, pain, suffering, discomfort }: Affliction) {
  return (
    <div className="bg-white p-3">
      <div className="flex items-center mb-2">
        <h3 className="font-bold uppercase text-sm">{title}</h3>
      </div>
      <div className="flex justify-center text-xs ">
        <div className="flex justify-center items-center normal-case gap-1 pr-2">
          <span className="font-bold">{percent}</span>
          <span className="font-bold">{text}</span>
        </div>
        <div className="flex items-center justify-end w-1/2">
          <div className="text-[9px] normal-case mx-auto">
            <div className="grid grid-cols-2 grid-rows-2 text-xs font-normal text-left normal-case mx-auto">
              <div className="bg-[#3C1212] text-white p-2">{agony}</div>
              <div className="bg-[#FF7B7B] text-[#3C1212] p-2">{pain}</div>
              <div className="bg-[#FFC3C3] text-[#3C1212] p-2">{suffering}</div>
              <div className="bg-[#FFE9E9] text-[#3C1212] p-2">{discomfort}</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
