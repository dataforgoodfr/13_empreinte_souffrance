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

interface AnimatedAfflictionsGroupProps {
  afflictions: Affliction[];
  delay?: number;
  cascade?: number;
}

export function AnimatedAfflictionsGroup({ afflictions, delay = 4000, cascade = 250 }: AnimatedAfflictionsGroupProps) {
  const [index, setIndex] = useState(0);

  useEffect(() => {
    const timer = setInterval(() => {
      setIndex((prev) => (prev + 1) % afflictions.length);
    }, delay);
    return () => clearInterval(timer);
  }, [afflictions.length, delay]);

  return (
    <div>
      {[0, 1, 2].map((offset, idx, arr) => (
        <div key={offset}>
          <AnimatedCard afflictions={afflictions} index={index} offset={offset} cascade={cascade} />
          {idx < arr.length - 0 && (
            <div className="bg-[#E7E4FF] text-center text-3xl font-extrabold w-full py-1">+</div>
          )}
        </div>
      ))}
    </div>
  );
}

interface AnimatedCardProps {
  afflictions: Affliction[];
  index: number;
  offset: number;
  cascade: number;
}

export function AnimatedCard({ afflictions, index, offset, cascade }: AnimatedCardProps) {
  const [current, setCurrent] = useState((index + offset) % afflictions.length);
  const [next, setNext] = useState<number | null>(null);
  const [anim, setAnim] = useState(false);
  const [entering, setEntering] = useState(false);
  const timeoutRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  useEffect(() => {
    const target = (index + offset) % afflictions.length;
    if (target !== current) {
      timeoutRef.current = setTimeout(() => {
        setNext(target);
        setAnim(true);
        setEntering(false);

        setTimeout(() => {
          setEntering(true);
        }, 10);

        setTimeout(() => {
          setCurrent(target);
          setNext(null);
          setAnim(false);
        }, 510);
      }, offset * cascade);
    }
    return () => {
      if (timeoutRef.current) clearTimeout(timeoutRef.current);
    };
  }, [index, offset, cascade, current, afflictions.length]);

  return (
    <div className="relative w-full min-h-[140px] overflow-hidden bg-white">
      {anim && (
        <div
          className={`absolute left-0 top-0 w-full z-1
            transition-transform duration-500
            -translate-x-full
            ${entering ? 'translate-x-full' : 'translate-x-0'}

          `}
          style={{ pointerEvents: 'none' }}
        >
          <SynteseSurffering {...afflictions[current]} />
        </div>
      )}
      {anim && next !== null && (
        <div
          className={`
            absolute left-0 top-0 w-full z-2
            transition-transform duration-500
            ${entering ? 'translate-x-0' : 'translate-x-full'}
          `}
          style={{ pointerEvents: 'none' }}
        >
          <SynteseSurffering {...afflictions[next]} />
        </div>
      )}
      {!anim && (
        <div className="absolute left-0 top-0 w-full z-1">
          <SynteseSurffering {...afflictions[current]} />
        </div>
      )}
    </div>
  );
}

function SynteseSurffering(props: Affliction) {
  const { title, percent, text, agony, pain, suffering, discomfort } = props;
  return (
    <div className="bg-white p-3">
      <div className="flex items-center mb-2">
        <h3 className="font-bold uppercase text-sm">{title}</h3>
      </div>

      <div className="flex justify-center text-xs ">
        <div className="flex justify-center items-center normal-case gap-1 mr-4">
          <span className="font-bold">{percent}</span>
          <span className="font-bold">{text}</span>
        </div>

        <div className="text-[9px] normal-case ml-4">
          <div className="grid grid-cols-2 grid-rows-2 text-xs font-normal normal-case">
            <div className="bg-[#3C1212] text-white p-2 sm:w-35">{agony}</div>
            <div className="bg-[#FF7B7B] text-[#3C1212] p-2 sm:w-35">{pain}</div>
            <div className="bg-[#FFC3C3] text-[#3C1212] p-2 sm:w-35">{suffering}</div>
            <div className="bg-[#FFE9E9] text-[#3C1212] p-2 sm:w-35">{discomfort}</div>
          </div>
        </div>
      </div>
    </div>
  );
}
