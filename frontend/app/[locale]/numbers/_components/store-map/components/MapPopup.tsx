'use client';

import type { MapColors, Store } from '../types';
import { COLORS } from '../types';

type MapPopupProps = {
  store: Store;
  colors?: MapColors;
};

export default function MapPopup({ store: s, colors = COLORS }: MapPopupProps) {
  const isCage = s.hasCageEggs;
  const accent = isCage ? colors.cage : colors.noCage;

  return (
    <div style={{ minWidth: 170, maxWidth: 220 }}>
      <p className="!m-0 font-bold text-[13px] leading-tight" style={{ color: '#1a1a2e' }}>
        {s.name}
      </p>

      <p className="!m-0 text-[10.5px] text-gray-400 leading-snug mt-0.5">{s.address}</p>

      <div className="my-2 h-px" style={{ backgroundColor: `${accent}30` }} />

      <div className="flex items-center gap-1.5">
        <span className="w-2 h-2 rounded-full shrink-0" style={{ backgroundColor: accent }} />
        <span className="text-[11.5px] font-semibold leading-none" style={{ color: accent }}>
          {isCage ? "Présence d'œufs cage" : "Pas d'œufs cage trouvés"}
        </span>
      </div>

      {s.nbRef > 0 && (
        <p className="!m-0 text-[10.5px] text-gray-400 mt-1.5">
          {s.nbRef} référence{s.nbRef > 1 ? 's' : ''} relevée{s.nbRef > 1 ? 's' : ''}
        </p>
      )}

      {s.urlImg && (
        <a
          href={s.urlImg}
          target="_blank"
          rel="noopener noreferrer"
          className="inline-flex items-center gap-1 mt-2 text-[10.5px] font-medium hover:underline"
          style={{ color: accent }}
        >
          <svg width="11" height="11" viewBox="0 0 16 16" fill="none" className="shrink-0">
            <rect x="1.5" y="2.5" width="13" height="11" rx="2" stroke="currentColor" strokeWidth="1.3" />
            <circle cx="5.5" cy="6.5" r="1.5" stroke="currentColor" strokeWidth="1" />
            <path
              d="M1.5 11l4-3 3 2 2.5-2L14.5 12"
              stroke="currentColor"
              strokeWidth="1.3"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
          </svg>
          Voir la photo
        </a>
      )}
    </div>
  );
}
