'use client';
import { useEffect, useRef, useState } from 'react';
import SufferingScales from '@/app/[locale]/methodology/_components/suffering-scales';
import BoltIconV2 from '../../ui/_components/BoltIconV2';

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
            <div className="bg-violet rounded-[5px] p-2 my-4 text-center text-3xl font-extrabold w-full">+</div>
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
    <div className="relative bg-white rounded-[5px] min-h-[200px] overflow-hidden">
      {anim && (
        <div
          className={`absolute left-0 top-0 w-full z-1
            transition-transform duration-500
            -translate-x-full
            ${entering ? 'translate-x-full' : 'translate-x-0'}

          `}
          style={{ pointerEvents: 'none' }}
        >
          <SufferingSynthesis {...afflictions[current]} />
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
          <SufferingSynthesis {...afflictions[next]} />
        </div>
      )}
      {!anim && (
        <div className="absolute left-0 top-0 w-full z-1">
          <SufferingSynthesis {...afflictions[current]} />
        </div>
      )}
    </div>
  );
}

function SufferingSynthesis(props: Affliction) {
  const { title, percent, text, agony, pain, suffering, discomfort } = props;
  return (
    <div className="p-4 w-full min-h-[200px] p-2 flex flex-col items-left justify-center bg-white gap-4 ">
      <div className="flex gap-2 items-center">
        <BoltIconV2 className="text-pink-3 h-[30px]" />
        <p className="text-caption text-center font-bold uppercase ">{title}</p>
      </div>

      <div className="grid grid-cols-2 text-caption ">
        <div className="flex flex-wrap justify-left items-center normal-case gap-1">
          <p className="p-2 flex justify-center items-left font-bold text-center">
            {percent} {text}
          </p>
        </div>

        <div className="w-full grid grid-cols-2 grid-rows-2 normal-case text-center">
          <SufferingScales
            agony_duration_text={agony}
            pain_duration_text={pain}
            suffering_duration_text={suffering}
            discomfort_duration_text={discomfort}
          />
        </div>
      </div>
    </div>
  );
}
