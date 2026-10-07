// Ordre d'affichage choisi par le joueur (07/10/2026) : pur affichage, local,
// jamais envoye au moteur. Un groupe de cartes (une rangee) ou la pile
// d'ameliorations d'une carte garde une liste d'identifiants ; les cartes
// absentes de la liste (arrivees depuis) suivent, dans leur ordre naturel.

export type Ordres = Record<string, number[]>

/** Clef d'une rangee : l'emplacement, son proprietaire, son secteur, son rang. */
export function cleDeRangee(
  emplacement: string,
  index: number,
  proprietaire?: number,
  secteur?: string
): string {
  return `${emplacement}|${proprietaire ?? ''}|${secteur ?? ''}|${index}`
}

/** Clef de la pile d'ameliorations d'une carte. */
export const cleDePile = (porteurId: number): string => `ameliorations|${porteurId}`

/** Range `elements` selon `ordre` ; les inconnus gardent leur ordre, apres. */
export function ranger<T>(elements: T[], idDe: (element: T) => number, ordre: number[] | undefined): T[] {
  if (!ordre || ordre.length === 0 || elements.length < 2) return elements
  const rang = new Map(ordre.map((id, i) => [id, i]))
  const connus = elements.filter((e) => rang.has(idDe(e))).sort((a, b) => rang.get(idDe(a))! - rang.get(idDe(b))!)
  const inconnus = elements.filter((e) => !rang.has(idDe(e)))
  return [...connus, ...inconnus]
}

/**
 * Nouvel ordre apres avoir pose `sourceId` avant (ou apres) `cibleId`.
 * `ids` est l'ordre actuellement affiche. Renvoie `ids` tel quel si rien ne change.
 */
export function deplacer(ids: number[], sourceId: number, cibleId: number, apres: boolean): number[] {
  if (sourceId === cibleId || !ids.includes(sourceId) || !ids.includes(cibleId)) return ids
  const sans = ids.filter((id) => id !== sourceId)
  const position = sans.indexOf(cibleId) + (apres ? 1 : 0)
  const resultat = [...sans.slice(0, position), sourceId, ...sans.slice(position)]
  return resultat.every((id, i) => id === ids[i]) ? ids : resultat
}

/** Une carte voisine, avec le centre de son rectangle a l'ecran. */
export type Voisine = { id: number; cx: number; cy: number }

/**
 * La voisine la plus proche du pointeur, et de quel cote le poser.
 * « Apres » quand le pointeur est a droite du centre de la voisine.
 */
export function placeVisee(
  voisines: Voisine[],
  x: number,
  y: number
): { cibleId: number; apres: boolean } | undefined {
  let meilleure: Voisine | undefined
  let distance = Infinity
  for (const v of voisines) {
    const d = Math.hypot(v.cx - x, v.cy - y)
    if (d < distance) {
      distance = d
      meilleure = v
    }
  }
  return meilleure ? { cibleId: meilleure.id, apres: x > meilleure.cx } : undefined
}
