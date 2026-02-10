import L from 'leaflet';
import type { MapColors, MarkerStyle } from './types';
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

/** Which SVG variant to use for a given style + cage/free type. */
function getSvgSrc(variant: 'default' | 'noborder' | 'inverted', type: 'cage' | 'free'): string {
  if (variant === 'noborder') return type === 'cage' ? MARKER_ICONS.cageNoBorder : MARKER_ICONS.freeNoBorder;
  if (variant === 'inverted') return type === 'cage' ? MARKER_ICONS.cageInverted : MARKER_ICONS.freeInverted;
  return type === 'cage' ? MARKER_ICONS.cage : MARKER_ICONS.free;
}

function circleSvg(fill: string, stroke: string, size: number, outline: boolean): string {
  const r = size / 2 - 1;
  const strokeAttr = outline ? `stroke="${stroke}" stroke-width="1.5"` : '';
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
  outline: boolean
): L.DivIcon {
  const key = `illustrated-${variant}|${type}|${w}|${h}|${outline}`;
  const cached = iconCache.get(key);
  if (cached) return cached;

  const src = getSvgSrc(variant, type);
  const styles = `width:${w}px;height:${h}px`;
  const cssClass = outline ? 'egg-marker' : 'egg-marker egg-marker--no-outline';
  const icon = L.divIcon({
    html: `<img src="${src}" width="${w}" height="${h}" style="${styles}" alt="" />`,
    className: cssClass,
    iconSize: [w, h],
    iconAnchor: [w / 2, h],
    popupAnchor: [0, -(h - 2)],
  });

  iconCache.set(key, icon);
  return icon;
}

function createCircleIcon(fill: string, stroke: string, size: number, outline: boolean): L.DivIcon {
  const key = `circle|${fill}|${stroke}|${size}|${outline}`;
  const cached = iconCache.get(key);
  if (cached) return cached;

  const svgHtml = circleSvg(fill, stroke, size, outline);
  const cssClass = outline ? 'egg-marker' : 'egg-marker egg-marker--no-outline';
  const icon = L.divIcon({
    html: svgHtml,
    className: cssClass,
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
  outline = true,
  colors: MapColors = COLORS
): { cage: L.DivIcon; free: L.DivIcon } {
  const h = markerSize;
  const w = Math.round(h * MARKER_ASPECT);

  switch (style) {
    case 'illustrated':
      return {
        cage: createIllustratedIcon('default', 'cage', w, h, outline),
        free: createIllustratedIcon('default', 'free', w, h, outline),
      };
    case 'illustrated-noborder':
      return {
        cage: createIllustratedIcon('noborder', 'cage', w, h, outline),
        free: createIllustratedIcon('noborder', 'free', w, h, outline),
      };
    case 'illustrated-mixed':
      return {
        cage: createIllustratedIcon('inverted', 'cage', w, h, outline),
        free: createIllustratedIcon('inverted', 'free', w, h, outline),
      };
    case 'circle': {
      const size = Math.min(w, h);
      return {
        cage: createCircleIcon(colors.cage, colors.cageStroke, size, outline),
        free: createCircleIcon(colors.noCage, colors.noCageStroke, size, outline),
      };
    }
  }
}
