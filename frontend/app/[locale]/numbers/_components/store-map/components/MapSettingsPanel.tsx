'use client';

import { useState } from 'react';
import type { MapColors, MarkerStyle } from '../types';
import { COLORS } from '../types';
import clsx from 'clsx';

const STYLE_OPTIONS: { id: MarkerStyle; label: string }[] = [
  { id: 'illustrated', label: 'Illustrés' },
  { id: 'illustrated-noborder', label: 'Sans contour' },
  { id: 'illustrated-inverted', label: 'Inversés' },
  { id: 'illustrated-mixed', label: 'Mixte' },
  { id: 'illustrated-mixed2', label: 'Mixte 2' },
  { id: 'egg', label: 'Œufs unis' },
  { id: 'circle', label: 'Cercles' },
];

const ILLUSTRATED_ICONS = {
  cage: '/logo/marker_cage_egg.svg',
  free: '/logo/marker_free_egg.svg',
  cageNoBorder: '/logo/marker_cage_egg_noborder.svg',
  freeNoBorder: '/logo/marker_free_egg_noborder.svg',
  cageInverted: '/logo/marker_cage_egg_inverted.svg',
  freeInverted: '/logo/marker_free_egg_inverted.svg',
} as const;

function ImgPair({ cage, free }: { cage: string; free: string }) {
  return (
    <span className="inline-flex items-end gap-1">
      <img src={cage} alt="" className="w-[16px] h-[20px]" />
      <img src={free} alt="" className="w-[16px] h-[20px]" />
    </span>
  );
}

function SvgEggPair({ colors }: { colors: MapColors }) {
  const egg = (fill: string, stroke: string) => (
    <svg width="14" height="18" viewBox="0 0 20 26" xmlns="http://www.w3.org/2000/svg">
      <path
        d="M10 0.5C15.52 0.5 19.5 9.07 19.5 15.77C19.5 22.47 15.52 25.5 10 25.5C4.48 25.5 0.5 22.47 0.5 15.77C0.5 9.07 4.48 0.5 10 0.5Z"
        fill={fill}
        stroke={stroke}
        strokeWidth="1"
      />
    </svg>
  );
  return (
    <span className="inline-flex items-end gap-1">
      {egg(colors.cage, colors.cageStroke)}
      {egg(colors.noCage, colors.noCageStroke)}
    </span>
  );
}

function SvgCirclePair({ colors }: { colors: MapColors }) {
  const circle = (fill: string, stroke: string) => (
    <svg width="14" height="14" viewBox="0 0 14 14" xmlns="http://www.w3.org/2000/svg">
      <circle cx="7" cy="7" r="6" fill={fill} stroke={stroke} strokeWidth="1.5" />
    </svg>
  );
  return (
    <span className="inline-flex items-center gap-1">
      {circle(colors.cage, colors.cageStroke)}
      {circle(colors.noCage, colors.noCageStroke)}
    </span>
  );
}

function StylePreview({ style, colors }: { style: MarkerStyle; colors: MapColors }) {
  const I = ILLUSTRATED_ICONS;
  switch (style) {
    case 'illustrated':
      return <ImgPair cage={I.cage} free={I.free} />;
    case 'illustrated-noborder':
      return <ImgPair cage={I.cageNoBorder} free={I.freeNoBorder} />;
    case 'illustrated-inverted':
      return <ImgPair cage={I.cageInverted} free={I.freeInverted} />;
    case 'illustrated-mixed':
      return <ImgPair cage={I.cageInverted} free={I.freeNoBorder} />;
    case 'illustrated-mixed2':
      return <ImgPair cage={I.cageInverted} free={I.freeInverted} />;
    case 'egg':
      return <SvgEggPair colors={colors} />;
    case 'circle':
      return <SvgCirclePair colors={colors} />;
  }
}

function SectionLabel({ children }: { children: string }) {
  return <p className="text-[9px] uppercase tracking-widest text-gray-400 font-bold px-2.5 pt-2.5 pb-1">{children}</p>;
}

function Divider() {
  return <div className="h-px bg-gray-100 mx-2.5" />;
}

function GearIcon() {
  return (
    <svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg" className="shrink-0">
      <path
        d="M6.5 1.5L6.8 3.1C6.3 3.3 5.8 3.6 5.4 4L3.8 3.4L2.3 5.9L3.6 7C3.5 7.3 3.5 7.7 3.5 8C3.5 8.3 3.5 8.7 3.6 9L2.3 10.1L3.8 12.6L5.4 12C5.8 12.4 6.3 12.7 6.8 12.9L6.5 14.5H9.5L9.2 12.9C9.7 12.7 10.2 12.4 10.6 12L12.2 12.6L13.7 10.1L12.4 9C12.5 8.7 12.5 8.3 12.5 8C12.5 7.7 12.5 7.3 12.4 7L13.7 5.9L12.2 3.4L10.6 4C10.2 3.6 9.7 3.3 9.2 3.1L9.5 1.5H6.5Z"
        stroke="currentColor"
        strokeWidth="1.2"
        strokeLinejoin="round"
      />
      <circle cx="8" cy="8" r="2" stroke="currentColor" strokeWidth="1.2" />
    </svg>
  );
}

type MapSettingsPanelProps = {
  currentStyle: MarkerStyle;
  // eslint-disable-next-line no-unused-vars
  onChangeStyle: (style: MarkerStyle) => void;
  markerSize: number;
  // eslint-disable-next-line no-unused-vars
  onChangeMarkerSize: (size: number) => void;
  markerOpacity: number;
  // eslint-disable-next-line no-unused-vars
  onChangeMarkerOpacity: (opacity: number) => void;
  showOutline: boolean;
  // eslint-disable-next-line no-unused-vars
  onToggleOutline: (show: boolean) => void;
  zoomScale: number;
  // eslint-disable-next-line no-unused-vars
  onChangeZoomScale: (scale: number) => void;
  colors?: MapColors;
};

export default function MapSettingsPanel({
  currentStyle,
  onChangeStyle,
  markerSize,
  onChangeMarkerSize,
  markerOpacity,
  onChangeMarkerOpacity,
  showOutline,
  onToggleOutline,
  zoomScale,
  onChangeZoomScale,
  colors = COLORS,
}: MapSettingsPanelProps) {
  const [open, setOpen] = useState(false);

  return (
    <div className="absolute top-3 right-3 z-[2]">
      <button
        onClick={() => setOpen((o) => !o)}
        title="Paramètres de la carte"
        className={clsx(
          'flex items-center justify-center',
          'w-8 h-8 rounded-full',
          'bg-white/90 backdrop-blur-md shadow-lg border border-white/60',
          'text-gray-500 hover:text-gray-700 hover:shadow-xl',
          'transition-all duration-200 cursor-pointer select-none',
          open && 'ring-2 ring-gray-300'
        )}
      >
        <GearIcon />
      </button>
      {open && (
        <div className="absolute top-10 right-0 mt-1 w-[210px] bg-white/95 backdrop-blur-md rounded-xl shadow-xl border border-gray-100 overflow-hidden">
          <div className="flex items-center justify-between px-3 pt-2.5 pb-1">
            <p className="text-[11px] font-bold text-gray-700">Paramètres</p>
            <button
              onClick={() => setOpen(false)}
              className="text-gray-400 hover:text-gray-600 transition-colors cursor-pointer p-0.5"
              title="Fermer"
            >
              <svg width="12" height="12" viewBox="0 0 12 12" fill="none">
                <path d="M2 2L10 10M10 2L2 10" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
              </svg>
            </button>
          </div>

          <SectionLabel>Marqueurs</SectionLabel>
          <div className="px-2 pb-1.5 flex flex-col gap-0.5">
            {STYLE_OPTIONS.map(({ id, label }) => {
              const isActive = currentStyle === id;
              return (
                <button
                  key={id}
                  onClick={() => onChangeStyle(id)}
                  className={clsx(
                    'flex items-center gap-2 w-full px-2 py-1.5 rounded-lg',
                    'text-left text-[11px] font-medium transition-all duration-150 cursor-pointer select-none',
                    isActive ? 'bg-gray-100 text-gray-900' : 'text-gray-500 hover:bg-gray-50 hover:text-gray-700'
                  )}
                >
                  <span
                    className={clsx(
                      'w-3 h-3 rounded-full border-[1.5px] shrink-0 flex items-center justify-center',
                      isActive ? 'border-gray-700' : 'border-gray-300'
                    )}
                  >
                    {isActive && <span className="w-1.5 h-1.5 rounded-full bg-gray-700" />}
                  </span>
                  <StylePreview style={id} colors={colors} />
                  <span className="flex-1">{label}</span>
                </button>
              );
            })}
          </div>

          <Divider />

          <div className="px-2.5 py-2 flex items-center justify-between">
            <span className="text-[11px] font-medium text-gray-600">Contours</span>
            <button
              onClick={() => onToggleOutline(!showOutline)}
              className={clsx(
                'relative w-8 h-[18px] rounded-full transition-colors duration-200 cursor-pointer',
                showOutline ? 'bg-gray-800' : 'bg-gray-300'
              )}
              role="switch"
              aria-checked={showOutline}
            >
              <span
                className={clsx(
                  'absolute top-[2px] w-[14px] h-[14px] rounded-full bg-white shadow-sm transition-transform duration-200',
                  showOutline ? 'translate-x-[16px]' : 'translate-x-[2px]'
                )}
              />
            </button>
          </div>

          <Divider />

          <SectionLabel>Taille</SectionLabel>
          <div className="px-2.5 pb-2">
            <div className="flex items-center gap-2">
              <input
                type="range"
                min={10}
                max={60}
                step={1}
                value={markerSize}
                onChange={(e) => onChangeMarkerSize(Number(e.target.value))}
                className="flex-1 h-1 accent-gray-700 cursor-pointer"
              />
              <span className="text-[10px] font-mono font-semibold text-gray-500 w-[30px] text-right">
                {markerSize}px
              </span>
            </div>
          </div>

          <Divider />

          <SectionLabel>Opacité</SectionLabel>
          <div className="px-2.5 pb-2">
            <div className="flex items-center gap-2">
              <input
                type="range"
                min={20}
                max={100}
                step={5}
                value={Math.round(markerOpacity * 100)}
                onChange={(e) => onChangeMarkerOpacity(Number(e.target.value) / 100)}
                className="flex-1 h-1 accent-gray-700 cursor-pointer"
              />
              <span className="text-[10px] font-mono font-semibold text-gray-500 w-[30px] text-right">
                {Math.round(markerOpacity * 100)}%
              </span>
            </div>
          </div>

          <Divider />

          <SectionLabel>Zoom adaptatif</SectionLabel>
          <div className="px-2.5 pb-2">
            <div className="flex items-center gap-2">
              <input
                type="range"
                min={0}
                max={100}
                step={5}
                value={Math.round(zoomScale * 100)}
                onChange={(e) => onChangeZoomScale(Number(e.target.value) / 100)}
                className="flex-1 h-1 accent-gray-700 cursor-pointer"
              />
              <span className="text-[10px] font-mono font-semibold text-gray-500 w-[30px] text-right">
                {zoomScale === 0 ? 'Off' : `${Math.round(zoomScale * 100)}%`}
              </span>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
