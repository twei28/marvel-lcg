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

/** La zone détectée, corrigée si une correction existe pour ce code d'image (forme rectangulaire : la pente est absorbée). */
export function corrigerZone(code: string, zone: ZoneTexte | null): ZoneTexte | null {
  const correction = ZONES_CORRECTIONS[code]
  if (!zone || !correction) return zone
  const corrigee = { ...zone, ...correction }
  return { ...corrigee, bords: [[corrigee.x0, corrigee.x1]] }
}
