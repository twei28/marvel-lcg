// La feuille de choix de cible au telephone se GLISSE au doigt (maquette approuvee par l'utilisateur, 26/10/2026) et se cale
// sur trois positions : REDUITE (poignee, titre, compteur : le plateau est presque entier a l'ecran), BASSE (tout, boutons
// compris) et HAUTE (plein cadre). Fonctions pures : le geste (pointer events) vit dans `FeuilleCibles.tsx`.

export type PositionFeuille = 'reduite' | 'basse' | 'haute'

/** Les decalages vers le BAS (px, depuis la position haute) de chaque position : plus c'est grand, plus la feuille est descendue. */
export type PositionsFeuille = Record<PositionFeuille, number>

/**
 * @param hauteur   hauteur totale de la feuille (px)
 * @param basse     hauteur VISIBLE voulue en position basse (tout le contenu, boutons compris)
 * @param reduite   hauteur VISIBLE voulue en position reduite (poignee, titre, compteur)
 */
export function positionsFeuille({ hauteur, basse, reduite }: { hauteur: number; basse: number; reduite: number }): PositionsFeuille {
  const h = Math.max(0, hauteur)
  return {
    haute: 0,
    basse: Math.max(0, h - basse),
    reduite: Math.max(0, h - reduite),
  }
}

/** Le decalage tenu entre la position haute et la position reduite : le doigt ne sort jamais la feuille de l'ecran. */
export function borner(decalage: number, positions: PositionsFeuille): number {
  return Math.min(positions.reduite, Math.max(positions.haute, decalage))
}

/** Combien d'images d'elan on prete au geste : la feuille continue un peu apres le relachement, comme un doigt qui lance. */
const IMAGES_D_ELAN = 8

/**
 * La position ou la feuille se cale au relachement : la plus proche du point ou elle IRAIT avec son elan.
 *
 * @param decalage  ou elle est au relachement (px depuis le haut)
 * @param vitesse   px par image au moment du relachement (negatif = vers le haut)
 */
export function caler(decalage: number, vitesse: number, positions: PositionsFeuille): PositionFeuille {
  const projete = decalage + vitesse * IMAGES_D_ELAN
  let meilleure: PositionFeuille = 'basse'
  let ecart = Number.POSITIVE_INFINITY
  for (const nom of ['haute', 'basse', 'reduite'] as const) {
    const distance = Math.abs(positions[nom] - projete)
    if (distance < ecart) {
      ecart = distance
      meilleure = nom
    }
  }
  return meilleure
}
