import L from 'leaflet';
import type { MapColors, MarkerStyle, OutlineMode } from './types';
import { COLORS } from './types';

const MARKER_ASPECT = 22 / 28;

const MARKER_ICONS = {
  cage: '/logo/marker_cage_egg.svg',
  free: '/logo/marker_free_egg.svg',
  cageNoBorder: '/logo/marker_cage_egg_noborder.svg',
  freeNoBorder: '/logo/marker_free_egg_noborder.svg',
  cageInverted: '/logo/marker_cage_egg_inverted.svg',
  freeInverted: '/logo/marker_free_egg_inverted.svg',
} as const;

function getSvgSrc(variant: 'default' | 'noborder' | 'inverted', type: 'cage' | 'free'): string {
  if (variant === 'noborder') return type === 'cage' ? MARKER_ICONS.cageNoBorder : MARKER_ICONS.freeNoBorder;
  if (variant === 'inverted') return type === 'cage' ? MARKER_ICONS.cageInverted : MARKER_ICONS.freeInverted;
  return type === 'cage' ? MARKER_ICONS.cage : MARKER_ICONS.free;
}

/** Map OutlineMode → CSS class for the marker div. */
function outlineCssClass(mode: OutlineMode): string {
  switch (mode) {
    case 'shadow':
      return 'egg-marker';
    case 'stroke':
      return 'egg-marker egg-marker--stroke';
    case 'none':
      return 'egg-marker egg-marker--no-outline';
  }
}

function circleSvg(fill: string, stroke: string, size: number, mode: OutlineMode, sw: number): string {
  const r = size / 2 - 1;
  // For circles, 'stroke' mode uses a black SVG stroke scaled by sw; 'shadow' uses the brand-color stroke
  const svgStrokeWidth = mode === 'stroke' ? (sw * 3.75).toFixed(2) : '1.5';
  const strokeAttr =
    mode === 'stroke'
      ? `stroke="#1a1a2e" stroke-width="${svgStrokeWidth}"`
      : mode === 'shadow'
        ? `stroke="${stroke}" stroke-width="1.5"`
        : '';
  return (
    `<svg xmlns="http://www.w3.org/2000/svg" width="${size}" height="${size}" viewBox="0 0 ${size} ${size}">` +
    `<circle cx="${size / 2}" cy="${size / 2}" r="${r}" fill="${fill}" ${strokeAttr}/>` +
    `</svg>`
  );
}

const iconCache = new Map<string, L.DivIcon>();

function createIllustratedIcon(
  variant: 'default' | 'noborder' | 'inverted',
  type: 'cage' | 'free',
  w: number,
  h: number,
  mode: OutlineMode
): L.DivIcon {
  const key = `illustrated-${variant}|${type}|${w}|${h}|${mode}`;
  const cached = iconCache.get(key);
  if (cached) return cached;

  const src = getSvgSrc(variant, type);
  const styles = `width:${w}px;height:${h}px`;
  const icon = L.divIcon({
    html: `<img src="${src}" width="${w}" height="${h}" style="${styles}" alt="" />`,
    className: outlineCssClass(mode),
    iconSize: [w, h],
    iconAnchor: [w / 2, h],
    popupAnchor: [0, -(h - 2)],
  });

  iconCache.set(key, icon);
  return icon;
}

function createCircleIcon(fill: string, stroke: string, size: number, mode: OutlineMode, sw: number): L.DivIcon {
  const key = `circle|${fill}|${stroke}|${size}|${mode}|${sw}`;
  const cached = iconCache.get(key);
  if (cached) return cached;

  const svgHtml = circleSvg(fill, stroke, size, mode, sw);
  const icon = L.divIcon({
    html: svgHtml,
    className: outlineCssClass(mode),
    iconSize: [size, size],
    iconAnchor: [size / 2, size / 2],
    popupAnchor: [0, -(size / 2)],
  });

  iconCache.set(key, icon);
  return icon;
}

export function createIconPairForStyle(
  style: MarkerStyle,
  markerSize: number,
  outlineMode: OutlineMode = 'none',
  colors: MapColors = COLORS,
  strokeWidth: number = 0.4
): { cage: L.DivIcon; free: L.DivIcon } {
  const h = markerSize;
  const w = Math.round(h * MARKER_ASPECT);

  switch (style) {
    case 'illustrated':
      return {
        cage: createIllustratedIcon('default', 'cage', w, h, outlineMode),
        free: createIllustratedIcon('default', 'free', w, h, outlineMode),
      };
    case 'illustrated-noborder':
      return {
        cage: createIllustratedIcon('noborder', 'cage', w, h, outlineMode),
        free: createIllustratedIcon('noborder', 'free', w, h, outlineMode),
      };
    case 'illustrated-mixed':
      return {
        cage: createIllustratedIcon('inverted', 'cage', w, h, outlineMode),
        free: createIllustratedIcon('inverted', 'free', w, h, outlineMode),
      };
    case 'circle': {
      const size = Math.min(w, h);
      return {
        cage: createCircleIcon(colors.cage, colors.cageStroke, size, outlineMode, strokeWidth),
        free: createCircleIcon(colors.noCage, colors.noCageStroke, size, outlineMode, strokeWidth),
      };
    }
  }
}
