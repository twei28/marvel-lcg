// Corrections À LA MAIN de la zone de texte détectée sur un scan (TraductionPosee) : seuls les bords donnés remplacent ceux
// de la détection, qui garde le reste (fond, gauche/droite). Mesurées sur l'image servie (assets/pics) : première et
// dernière ligne de l'intérieur clair du cadre de texte, autour de la zone détectée.
//
// The Vault (Kajislav, 25/10/2026) : le cadre de texte de ce gabarit est INCLINÉ ; la détection prend la première ligne
// entièrement claire, sous la pente, et laissait dépasser au-dessus du voile le haut de « Activation Order N » (méchants),
// des traits (TRAITOR, LOCATION) et, sous le voile, la fin de la citation de Craven Escape.
import type { ZoneTexte } from './traduction-posee'

export type CorrectionZone = Partial<Pick<ZoneTexte, 'x0' | 'y0' | 'x1' | 'y1'>>

const MECHANT_VAULT: CorrectionZone = { y0: 0.582, y1: 0.932 }

export const ZONES_CORRECTIONS: Readonly<Record<string, CorrectionZone>> = {
  ...Object.fromEntries(Array.from({ length: 16 }, (_, i) => [`vt${String(i + 1).padStart(3, '0')}`, MECHANT_VAULT])),
  vt018: { y0: 0.579, y1: 0.932 },
  vt019: { y0: 0.584, y1: 0.921 },
  vt020: { y0: 0.502, y1: 0.925 },
  vt022: { y0: 0.583, y1: 0.932 },
  vt030: { y0: 0.573, y1: 0.932 },
  vt034: { y0: 0.573, y1: 0.932 },
}

/**
 * Zones relevées À LA MAIN, pour les cartes dont le cadre de texte n'est pas du gris clair et que la détection ne trouve pas, ou
 * trouve de travers (audit du 25/10/2026) : cadres teintés, sombres, ou chargés. Elles REMPLACENT la détection.
 * Fractions de l'IMAGE (comme la détection) ; `coin` : le haut de la zone, sur la hauteur donnée, s'arrête à `x1` (un badge mord dessus).
 */
export type ZoneManuelle = {
  x0: number
  y0: number
  x1: number
  y1: number
  fond: [number, number, number]
  coin?: { hauteur: number; x1: number }
  /** Une illustration mord sur le cadre : jusqu'à `jusqua` (fraction de la HAUTEUR de la zone), le bord gauche ou droit est celui donné. Premier palier atteint. */
  paliers?: { jusqua: number; x0?: number; x1?: number }[]
}

export const ZONES_MANUELLES: Readonly<Record<string, ZoneManuelle>> = {
  ah007: { x0: 0.06, y0: 0.67, x1: 0.92, y1: 0.905, fond: [254, 254, 236] },
  ah012b: { x0: 0.05, y0: 0.575, x1: 0.93, y1: 0.885, fond: [254, 254, 238] },
  cd015: { x0: 0.045, y0: 0.56, x1: 0.935, y1: 0.88, fond: [52, 52, 52] },
  hs035: { x0: 0.04, y0: 0.62, x1: 0.95, y1: 0.925, fond: [250, 247, 237] },
  ma015: { x0: 0.05, y0: 0.645, x1: 0.95, y1: 0.89, fond: [233, 236, 239] },
  ma016: { x0: 0.05, y0: 0.645, x1: 0.95, y1: 0.89, fond: [233, 236, 239] },
  pu013: { x0: 0.05, y0: 0.575, x1: 0.94, y1: 0.895, fond: [251, 246, 245], coin: { hauteur: 0.17, x1: 0.77 } },
  pu090a: { x0: 0.06, y0: 0.465, x1: 0.93, y1: 0.905, fond: [253, 252, 252] },
  sk146: { x0: 0.175, y0: 0.49, x1: 0.945, y1: 0.915, fond: [226, 246, 233] },
  sk150: { x0: 0.165, y0: 0.495, x1: 0.955, y1: 0.915, fond: [226, 246, 233] },
  sk196: { x0: 0.18, y0: 0.5, x1: 0.95, y1: 0.915, fond: [224, 239, 225] },
  sk198: { x0: 0.18, y0: 0.5, x1: 0.95, y1: 0.915, fond: [224, 239, 225] },
  tk106: { x0: 0.03, y0: 0.60, x1: 0.97, y1: 0.915, fond: [237, 237, 238] },
  sr017: { x0: 0.03, y0: 0.57, x1: 0.95, y1: 0.9, fond: [241, 247, 233] },
  bt009: { x0: 0.05, y0: 0.7, x1: 0.95, y1: 0.905, fond: [252, 253, 254] },
  dd007: { x0: 0.04, y0: 0.695, x1: 0.955, y1: 0.91, fond: [253, 253, 253] },
  wd128: { x0: 0.04, y0: 0.69, x1: 0.955, y1: 0.91, fond: [244, 244, 244] },
  wd129: { x0: 0.04, y0: 0.69, x1: 0.955, y1: 0.91, fond: [244, 244, 244] },
  wd156: { x0: 0.04, y0: 0.69, x1: 0.955, y1: 0.91, fond: [242, 243, 243] },
  // Illustration qui mord sur le cadre (audit du 25/10/2026, planche de l'utilisateur) : le menton de Rhino sur tk010, une main sur
  // tk001a/tk002a, le badge « 2 » de Ms. Lion, le bouclier de Nendo, le bâton d'Onmitsu (cadre rétréci sur toute la hauteur : le décor ne gère que l'encoche du haut).
  tk010: { x0: 0.035, y0: 0.515, x1: 0.845, y1: 0.915, fond: [254, 253, 248], paliers: [{ jusqua: 0.175, x0: 0.44 }] },
  tk001a: { x0: 0.04, y0: 0.575, x1: 0.88, y1: 0.915, fond: [254, 253, 248], paliers: [{ jusqua: 0.66, x1: 0.76 }] },
  tk002a: { x0: 0.04, y0: 0.575, x1: 0.88, y1: 0.915, fond: [254, 253, 248], paliers: [{ jusqua: 0.66, x1: 0.76 }] },
  sk170b: { x0: 0.03, y0: 0.575, x1: 0.955, y1: 0.925, fond: [238, 249, 231] },
  sk171b: { x0: 0.03, y0: 0.575, x1: 0.955, y1: 0.925, fond: [238, 249, 231] },
  sk172b: { x0: 0.04, y0: 0.575, x1: 0.955, y1: 0.925, fond: [238, 249, 231] },
  sk203: { x0: 0.04, y0: 0.575, x1: 0.965, y1: 0.925, fond: [233, 249, 234] },
  cd008: { x0: 0.14, y0: 0.585, x1: 0.945, y1: 0.905, fond: [248, 253, 255] },
  gs010: { x0: 0.115, y0: 0.585, x1: 0.965, y1: 0.905, fond: [255, 255, 255] },
  jj022: { x0: 0.045, y0: 0.585, x1: 0.955, y1: 0.915, fond: [254, 254, 254] },
  lj025: { x0: 0.04, y0: 0.585, x1: 0.955, y1: 0.925, fond: [254, 254, 254], paliers: [{ jusqua: 0.16, x1: 0.74 }] },
  pu104: { x0: 0.03, y0: 0.555, x1: 0.965, y1: 0.895, fond: [253, 252, 252] },
  sc001: { x0: 0.035, y0: 0.585, x1: 0.7, y1: 0.915, fond: [254, 254, 254] },
  se010: { x0: 0.04, y0: 0.585, x1: 0.7, y1: 0.915, fond: [251, 251, 252] },
  // Cadres plus hauts que la détection ne le voyait (un trait, une citation ou un titre d'environnement restait en anglais au-dessus du voile),
  // cadres pris pour une illustration (an010), titre rogné (sv010).
  sv010: { x0: 0.075, y0: 0.705, x1: 0.95, y1: 0.915, fond: [255, 255, 255] },
  an010: { x0: 0.03, y0: 0.575, x1: 0.965, y1: 0.92, fond: [255, 255, 255] },
  pu015: { x0: 0.1, y0: 0.575, x1: 0.88, y1: 0.895, fond: [251, 247, 246], coin: { hauteur: 0.16, x1: 0.72 } },
  pu140: { x0: 0.105, y0: 0.18, x1: 0.93, y1: 0.925, fond: [251, 246, 243] },
  pu144: { x0: 0.105, y0: 0.18, x1: 0.93, y1: 0.925, fond: [251, 246, 243] },
  pu147: { x0: 0.1, y0: 0.19, x1: 0.93, y1: 0.91, fond: [251, 246, 243] },
  wc021: { x0: 0.04, y0: 0.57, x1: 0.96, y1: 0.915, fond: [255, 254, 249] },
  wc022: { x0: 0.04, y0: 0.57, x1: 0.96, y1: 0.915, fond: [255, 254, 249] },
  60020: { x0: 0.04, y0: 0.59, x1: 0.945, y1: 0.915, fond: [253, 251, 238], coin: { hauteur: 0.18, x1: 0.75 } },
  // Manigance annexe paysage : le flavor anglais dépassait au-dessus du voile.
  hs021: { x0: 0.455, y0: 0.215, x1: 0.975, y1: 0.65, fond: [241, 234, 226] },
}

function zoneManuelle(m: ZoneManuelle): ZoneTexte {
  const lignes = 100
  const bords = Array.from({ length: lignes }, (_, i): [number, number] => {
    const palier = m.paliers?.find((p) => i / lignes < p.jusqua)
    return [palier?.x0 ?? m.x0, palier?.x1 ?? (m.coin && i / lignes < m.coin.hauteur ? m.coin.x1 : m.x1)]
  })
  return { x0: m.x0, y0: m.y0, x1: m.x1, y1: m.y1, fond: m.fond, bords }
}

/** La zone détectée, corrigée si une correction existe pour ce code d'image (forme rectangulaire : la pente est absorbée). */
export function corrigerZone(code: string, zone: ZoneTexte | null): ZoneTexte | null {
  const manuelle = ZONES_MANUELLES[code]
  if (manuelle) return zoneManuelle(manuelle)
  const correction = ZONES_CORRECTIONS[code]
  if (!zone || !correction) return zone
  const corrigee = { ...zone, ...correction }
  return { ...corrigee, bords: [[corrigee.x0, corrigee.x1]] }
}
