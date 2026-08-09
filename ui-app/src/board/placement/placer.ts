// Où poser un panneau flottant pour qu'il ne cache pas ce dont il parle.
//
// Fonction PURE : aucune lecture du DOM, aucune dépendance à React. Elle prend
// des rectangles et rend une position. C'est ce qui permet de la tester à fond
// sans navigateur, alors que le bug qu'elle corrige est éminemment visuel.
//
// Le principe : une liste ORDONNÉE de positions candidates, la première étant
// celle qu'on préfère. On note chacune, on garde la meilleure. Pas de recherche
// d'espace libre, pas d'optimisation continue — un jeu de positions connues
// donne un placement prévisible, et la prévisibilité vaut mieux que l'optimum
// pour un panneau qu'on cherche du regard.

import type { Boite } from './boites'

export type Ancre =
  | 'centre'
  | 'bas'
  | 'haut'
  | 'gauche'
  | 'droite'
  | 'bas-gauche'
  | 'bas-droite'
  | 'haut-gauche'
  | 'haut-droite'

/** Ordre d'essai par défaut : le centre d'abord, les coins en dernier ressort. */
export const CANDIDATS_PAR_DEFAUT: readonly Ancre[] = [
  'centre',
  'bas',
  'haut',
  'gauche',
  'droite',
  'bas-gauche',
  'bas-droite',
  'haut-gauche',
  'haut-droite',
]

export const MARGE_PAR_DEFAUT = 12

/**
 * Hauteur relative de l'ancre « centre ».
 *
 * 45 % et non 50 % : c'est la valeur qu'avaient les panneaux avant ce
 * changement, et la garder évite de déplacer le panneau dans tous les cas où il
 * ne gênait déjà personne.
 */
const CENTRE_Y = 0.45

/**
 * Le moindre recouvrement coûte plus cher que le plus grand déplacement.
 *
 * Une fenêtre fait au plus quelques milliers de pixels de diagonale, alors
 * qu'un pixel carré de recouvrement vaut déjà 1000 : aucune distance ne peut
 * racheter un panneau qui cache une carte. On ne recouvre donc que s'il
 * n'existe VRAIMENT aucune position libre.
 */
const POIDS_RECOUVREMENT = 1000

export type Taille = { w: number; h: number }

export type EntreePlacement = {
  /** Dimensions du panneau à poser. */
  taille: Taille
  /** Ce qu'il ne doit pas recouvrir : cartes concernées, panneaux déjà posés. */
  aEviter: readonly Boite[]
  viewport: Taille
  /** Position de repli et référence de distance. Défaut : le centre. */
  preferee?: Ancre
  marge?: number
  candidats?: readonly Ancre[]
  /**
   * Abscisse que le bord droit du panneau ne doit pas dépasser.
   *
   * Sert à tenir un panneau ancré à droite HORS d'une colonne de la table :
   * l'aperçu d'une carte seule est étroit, il n'a aucune raison de s'asseoir
   * sur la colonne des manigances. C'est une borne distincte de `marge`, et
   * c'est indispensable — `marge` vaut sur les DEUX axes, s'en servir pour
   * décaler horizontalement écraserait le centrage vertical.
   */
  borneDroite?: number
}

export type Placement = {
  /** Coin haut-gauche du panneau, dans le repère du viewport. */
  x: number
  y: number
  ancre: Ancre
  /**
   * Vrai quand même la meilleure position recouvre encore quelque chose. Le
   * panneau s'allège alors visuellement (voir la classe `est-genant`) : on ne
   * peut pas le mettre ailleurs, autant laisser lire au travers.
   */
  genant: boolean
}

/** Aire commune à deux rectangles. 0 s'ils ne se touchent pas. */
export function chevauchement(a: Boite, b: Boite): number {
  const largeur = Math.min(a.x + a.w, b.x + b.w) - Math.max(a.x, b.x)
  const hauteur = Math.min(a.y + a.h, b.y + b.h) - Math.max(a.y, b.y)
  return largeur > 0 && hauteur > 0 ? largeur * hauteur : 0
}

/**
 * Coin haut-gauche d'une ancre, borné au viewport.
 *
 * Un panneau plus grand que la fenêtre est collé à la marge haute-gauche plutôt
 * que centré sur un débordement symétrique : on préfère perdre le bas, qu'on
 * peut deviner, que le titre.
 */
function positionDe(
  ancre: Ancre,
  taille: Taille,
  viewport: Taille,
  marge: number,
  borneDroite?: number
): { x: number; y: number } {
  const centreX = (viewport.w - taille.w) / 2
  const centreY = viewport.h * CENTRE_Y - taille.h / 2
  const milieuY = (viewport.h - taille.h) / 2
  const gauche = marge
  const droite = viewport.w - taille.w - marge
  const haut = marge
  const bas = viewport.h - taille.h - marge

  const brut = {
    centre: { x: centreX, y: centreY },
    bas: { x: centreX, y: bas },
    haut: { x: centreX, y: haut },
    gauche: { x: gauche, y: milieuY },
    droite: { x: droite, y: milieuY },
    'bas-gauche': { x: gauche, y: bas },
    'bas-droite': { x: droite, y: bas },
    'haut-gauche': { x: gauche, y: haut },
    'haut-droite': { x: droite, y: haut },
  }[ancre]

  const xMaximum = Math.max(
    marge,
    Math.min(viewport.w - taille.w - marge, (borneDroite ?? Infinity) - taille.w)
  )
  return {
    x: borner(brut.x, marge, xMaximum),
    y: borner(brut.y, marge, Math.max(marge, viewport.h - taille.h - marge)),
  }
}

function borner(valeur: number, min: number, max: number): number {
  return Math.max(min, Math.min(max, valeur))
}

function distance(a: { x: number; y: number }, b: { x: number; y: number }): number {
  return Math.hypot(a.x - b.x, a.y - b.y)
}

/**
 * La meilleure position pour ce panneau.
 *
 * Déterministe : mêmes entrées, même sortie. À score égal c'est la position la
 * plus haute dans la liste des candidats qui gagne, jamais un hasard d'ordre de
 * parcours — un panneau qui changerait de place sans raison serait pire que
 * celui qui cache une carte.
 */
export function placer(entree: EntreePlacement): Placement {
  const marge = entree.marge ?? MARGE_PAR_DEFAUT
  const candidats = entree.candidats ?? CANDIDATS_PAR_DEFAUT
  const preferee = entree.preferee ?? 'centre'
  const reference = positionDe(preferee, entree.taille, entree.viewport, marge, entree.borneDroite)

  // La position préférée est toujours essayée en premier, même si elle ne
  // figure pas dans la liste : c'est le repli quand tout est occupé.
  const aEssayer: Ancre[] = [preferee, ...candidats.filter((a) => a !== preferee)]

  let meilleur: (Placement & { score: number }) | undefined
  for (const ancre of aEssayer) {
    const position = positionDe(ancre, entree.taille, entree.viewport, marge, entree.borneDroite)
    const boite: Boite = { ...position, ...entree.taille }
    const recouvrement = entree.aEviter.reduce((total, autre) => total + chevauchement(boite, autre), 0)
    const score = recouvrement * POIDS_RECOUVREMENT + distance(position, reference)
    if (!meilleur || score < meilleur.score) {
      meilleur = { ...position, ancre, genant: recouvrement > 0, score }
    }
    // Une position parfaitement libre ET préférée : inutile de chercher plus loin.
    if (score === 0) break
  }

  const { score: _score, ...placement } = meilleur as Placement & { score: number }
  return placement
}
