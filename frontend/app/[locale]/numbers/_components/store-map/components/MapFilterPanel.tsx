'use client';

import { useEffect, useState } from 'react';
import type { CageFilterValue, EnseigneConfig, MapColors } from '../types';
import { COLORS } from '../types';
import clsx from 'clsx';

/** Illustrated egg icons used in filter pill buttons. */
const FILTER_ICONS = {
  cage: '/logo/marker_cage_egg.svg',
  free: '/logo/marker_free_egg.svg',
} as const;

/** Breakpoint (px) below which mobile layout is used. */
const MOBILE_BP = 768;

function CageFilterButton({
  active,
  color,
  icon,
  label,
  onClick,
}: {
  active: boolean;
  color: string;
  icon: string;
  label: string;
  onClick: () => void;
}) {
  return (
    <button
      onClick={onClick}
      title={label}
      aria-pressed={active}
      className={clsx(
        'flex items-center gap-1 rounded-full pl-1.5 pr-2.5 py-1 text-[10px] md:text-[11px] font-bold',
        'border-2 transition-all duration-200 cursor-pointer select-none whitespace-nowrap',
        active
          ? 'shadow-md scale-[1.02]'
          : 'border-gray-200 bg-white text-gray-500 hover:border-gray-300 hover:shadow-sm'
      )}
      style={active ? { color, borderColor: color, backgroundColor: `${color}12` } : {}}
    >
      <img src={icon} alt="" className="w-[12px] h-[16px] md:w-[14px] md:h-[18px] shrink-0" />
      <span>{label}</span>
    </button>
  );
}

function EnseigneButton({
  enseigne,
  isSelected,
  onClick,
}: {
  enseigne: EnseigneConfig;
  isSelected: boolean;
  onClick: () => void;
}) {
  return (
    <button
      onClick={onClick}
      title={enseigne.name}
      aria-pressed={isSelected}
      className={clsx(
        'group flex items-center justify-center',
        'bg-transparent border-none p-0',
        'transition-all duration-200 cursor-pointer select-none',
        isSelected ? 'scale-[1.15]' : 'hover:scale-[1.1]'
      )}
    >
      <img
        alt={enseigne.name}
        src={enseigne.logo}
        className={clsx(
          'max-w-[36px] max-h-[32px] md:max-w-[44px] md:max-h-[38px] object-contain transition-all duration-200',
          isSelected
            ? 'brightness-110 saturate-110 drop-shadow-[0_2px_6px_rgba(0,0,0,0.3)]'
            : 'opacity-40 grayscale-[50%] group-hover:opacity-90 group-hover:grayscale-0 group-hover:drop-shadow-[0_1px_3px_rgba(0,0,0,0.15)]'
        )}
      />
    </button>
  );
}

function FilterIcon() {
  return (
    <svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg" className="shrink-0">
      <path
        d="M1.5 2.5H14.5L9.5 8.5V12.5L6.5 14V8.5L1.5 2.5Z"
        stroke="currentColor"
        strokeWidth="1.2"
        strokeLinejoin="round"
        strokeLinecap="round"
      />
    </svg>
  );
}

function ChevronDownIcon({ className }: { className?: string }) {
  return (
    <svg
      width="12"
      height="12"
      viewBox="0 0 12 12"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      className={className}
    >
      <path
        d="M3 4.5L6 7.5L9 4.5"
        stroke="currentColor"
        strokeWidth="1.5"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  );
}

type MapFilterPanelProps = {
  cageFilter: CageFilterValue;
  selectedEnseigne: string | null;
  enseigneList: EnseigneConfig[];
  // eslint-disable-next-line no-unused-vars
  onToggleCage: (value: CageFilterValue) => void;
  // eslint-disable-next-line no-unused-vars
  onToggleEnseigne: (id: string) => void;
  colors?: MapColors;
};

export default function MapFilterPanel({
  cageFilter,
  selectedEnseigne,
  enseigneList,
  onToggleCage,
  onToggleEnseigne,
  colors = COLORS,
}: MapFilterPanelProps) {
  const [isMobile, setIsMobile] = useState(false);
  const [expanded, setExpanded] = useState(true);

  useEffect(() => {
    const check = () => setIsMobile(window.innerWidth < MOBILE_BP);
    check();
    window.addEventListener('resize', check);
    return () => window.removeEventListener('resize', check);
  }, []);

  const hasActiveFilter = cageFilter !== 'all' || selectedEnseigne !== null;

  return (
    <div className="absolute bottom-3 left-3 z-[2] max-w-[calc(100%-24px)]">
      {isMobile && !expanded && (
        <button
          onClick={() => setExpanded(true)}
          title="Filtres"
          className={clsx(
            'relative flex items-center gap-1.5',
            'bg-white/90 backdrop-blur-md rounded-full shadow-lg border border-white/60',
            'px-3 py-2 text-gray-500 hover:text-gray-700 hover:shadow-xl',
            'transition-all duration-200 cursor-pointer select-none'
          )}
        >
          <FilterIcon />
          <span className="text-[11px] font-bold">Filtres</span>
          {hasActiveFilter && (
            <span className="absolute -top-1 -right-1 w-2.5 h-2.5 rounded-full bg-red-500 border-2 border-white" />
          )}
        </button>
      )}

      {expanded && (
        <div className="bg-white/90 backdrop-blur-md rounded-2xl shadow-lg border border-white/60 px-2.5 md:px-3 py-2">
          {isMobile && (
            <div className="flex items-center justify-between mb-1.5">
              <span className="text-[9px] uppercase tracking-widest text-gray-400 font-bold">Filtres</span>
              <button
                onClick={() => setExpanded(false)}
                className="text-gray-400 hover:text-gray-600 transition-colors cursor-pointer p-0.5"
                title="Réduire"
              >
                <ChevronDownIcon />
              </button>
            </div>
          )}

          <div className="flex items-center justify-around gap-1.5 mb-1.5">
            <CageFilterButton
              active={cageFilter === 'cage'}
              color={colors.cage}
              icon={FILTER_ICONS.cage}
              label="Présence d'œufs cage"
              onClick={() => onToggleCage('cage')}
            />
            <CageFilterButton
              active={cageFilter === 'noCage'}
              color={colors.noCage}
              icon={FILTER_ICONS.free}
              label="Pas d'œufs cage trouvés"
              onClick={() => onToggleCage('noCage')}
            />
          </div>

          <div className="h-px bg-gray-200/60 mb-1.5" />

          <div
            className="grid items-center justify-items-center"
            style={{ gridTemplateColumns: 'repeat(4, 1fr)', gap: '6px 0' }}
          >
            {enseigneList.map((enseigne) => (
              <div key={enseigne.id} className="flex items-center justify-center h-[36px] md:h-[44px]">
                <EnseigneButton
                  enseigne={enseigne}
                  isSelected={selectedEnseigne === enseigne.id}
                  onClick={() => onToggleEnseigne(enseigne.id)}
                />
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
