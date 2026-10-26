// Disposition ADAPTATIVE des zones de la table en ronds (26/10/2026, demande de l'utilisateur sur telephone : « on perd beaucoup de
// place sur les sbires et allies ; les zones devraient changer de taille en fonction du nombre de ronds » ; maquettes approuvees
// maquette-zones-adaptatives-telephone.html et maquette-colonnes-par-zone-telephone.html).
//
// Fonction PURE : elle part des comptes de ronds par zone, de la largeur et de la hauteur MESUREES du conteneur et du nombre de
// colonnes choisi pour chaque zone, et rend le diametre des ronds, les colonnes effectives et la largeur de chaque zone.
// Aucune mesure du DOM ici (TableRonds mesure et affine, voir `useDispositionRonds`).
//
// Geometrie reprise du CSS (ronds.css) :
//   - une rangee a 10 px de marge de chaque cote ; entre ses deux zones : 6 px de gouttiere, 1 px de separateur, 6 px de gouttiere
//     et 2 × 2 px de marge du separateur = 17 px ;
//   - une COLONNE a la largeur d'un rond : `d + 6` (`1,22 × d + 6` pour le mechant et le heros, plus 0,7 rond par amelioration
//     decalee sur le cote) ; 6 px entre deux colonnes ;
//   - donc une zone de `c` colonnes de coefficient `k` occupe `c × k × d + 12 × c − 6` px.
import type { CleZone } from './repartir-ronds'

/** 0 = Auto : jusqu'a 3 colonnes tant que les ronds restent a `D_AUTO_MIN` px ou plus. */
export type NbColonnes = 0 | 1 | 2 | 3 | 4

export type ColonnesZones = { manigances: NbColonnes; allies: NbColonnes; sbires: NbColonnes; enJeu: NbColonnes }

/** Retenu par l'utilisateur (26/10/2026) : Manigances 3, Allies 3, Sbires 3, Cartes en jeu 4 ; le mechant et le heros ont une seule colonne. */
export const COLONNES_PAR_DEFAUT: ColonnesZones = { manigances: 3, allies: 3, sbires: 3, enJeu: 4 }

/** Plus grand diametre, plus petit diametre (sous lequel l'ecran defile) et seuil de l'Auto. */
export const D_MAX = 76
export const D_MIN = 44
export const D_AUTO_MIN = 54
/** Ni stats ni pastilles lourdes sous ce diametre (le CSS masque ATK / SCH). */
export const D_AVEC_STATS = 54

export type EntreeZone = {
  /** Nombre de ronds de la zone. */
  n: number
  /** Le plus grand nombre d'ameliorations decalees sur le cote d'un rond de la zone (elles elargissent sa colonne). */
  amelios: number
}
export type Comptes = Record<CleZone, EntreeZone>

export type ZoneDisposee = {
  /** Colonnes reellement utilisees (0 pour une zone vide : elle se reduit a un bandeau). */
  colonnes: number
  /** Largeur de la zone en px. */
  largeur: number
  /** Largeur d'une colonne en px (un rond et ses ameliorations decalees). */
  largeurColonne: number
  vide: boolean
}
export type RangeeDisposee = { gauche: ZoneDisposee; droite: ZoneDisposee }

export type Disposition = {
  /** Diametre d'un rond ordinaire, en px (entier). */
  d: number
  rangees: [RangeeDisposee, RangeeDisposee, RangeeDisposee]
  /** Hauteur estimee de la table pour ce diametre. */
  hauteurEstimee: number
  /** Tout tient dans la hauteur donnee (sinon l'ecran defile verticalement : jamais horizontalement). */
  tient: boolean
}

type Entree = { largeur: number; hauteur: number; comptes: Comptes; colonnes: ColonnesZones }

const MARGE_RANGEE = 10
const SEPARATEUR = 17
const ECART_COLONNES = 6
const BANDEAU_VIDE = 78
const COEF_HEROS = 1.22
const DECALAGE_AMELIO = 0.7
/** Marges verticales du mode adaptatif (ronds.css `.est-adaptative`) : bas de table 14 px, rangee 4 + 6 px, 6 px entre deux lignes. */
const BAS_DE_TABLE = 14
const MARGES_RANGEE = 4 + 6
const ECART_LIGNES = 6

/** Le coefficient d'une zone : le mechant et le heros sont plus gros (1,22), et chaque amelioration decalee ajoute 0,7 rond. */
function coef(cle: CleZone, amelios: number): number {
  const base = cle === 'vilain' || cle === 'heros' ? COEF_HEROS : 1
  return base * (1 + DECALAGE_AMELIO * amelios)
}

const largeurZone = (colonnes: number, k: number, d: number): number =>
  colonnes === 0 ? BANDEAU_VIDE : colonnes * (k * d + 6) + (colonnes - 1) * ECART_COLONNES

/** Hauteur d'une zone de `n` ronds sur `colonnes` colonnes : titre, lignes de ronds (rond + nom + stats) et espacement. */
function hauteurZone(cle: CleZone, n: number, colonnes: number, d: number): number {
  const titre = 22 + 4
  if (n === 0 || colonnes === 0) return titre
  const dh = d * (cle === 'vilain' || cle === 'heros' ? COEF_HEROS : 1)
  const lignes = Math.ceil(n / colonnes)
  const ligne = dh + 2 + 20 + (d >= D_AVEC_STATS ? 14 : 0)
  return titre + lignes * ligne + (lignes - 1) * ECART_LIGNES
}

type Cles = ['vilain' | 'allies' | 'heros', 'manigances' | 'sbires' | 'enJeu']
const RANGEES: Cles[] = [
  ['vilain', 'manigances'],
  ['allies', 'sbires'],
  ['heros', 'enJeu'],
]

/** Les colonnes choisies pour une zone ; le mechant et le heros n'en ont qu'une. */
function colonnesChoisies(cle: CleZone, colonnes: ColonnesZones): NbColonnes {
  if (cle === 'vilain' || cle === 'heros') return 1
  return colonnes[cle]
}

/** Le diametre maximal pour que la rangee tienne en largeur, avec ces colonnes effectives. */
function dPourRangee(largeur: number, g: { cle: CleZone; n: number; amelios: number; colonnes: number }, dr: typeof g): number {
  const place = largeur - 2 * MARGE_RANGEE - SEPARATEUR
  let coefficients = 0
  let fixe = 0
  for (const z of [g, dr]) {
    if (z.colonnes === 0) {
      fixe += BANDEAU_VIDE
      continue
    }
    coefficients += z.colonnes * coef(z.cle, z.amelios)
    fixe += 12 * z.colonnes - 6
  }
  if (coefficients === 0) return D_MAX
  return (place - fixe) / coefficients
}

type ZoneEtat = { cle: CleZone; n: number; amelios: number; colonnes: number; auto: boolean; max: number }

function zoneEtat(cle: CleZone, e: Entree): ZoneEtat {
  const { n, amelios } = e.comptes[cle]
  const choix = colonnesChoisies(cle, e.colonnes)
  const auto = choix === 0
  const max = n === 0 ? 0 : Math.min(n, auto ? 3 : choix)
  return { cle, n, amelios, colonnes: max, auto, max }
}

/**
 * Resout les colonnes d'une rangee : en Auto, on garde le plus de colonnes (3 au plus) qui laissent des ronds >= 54 px ; et, dans tous
 * les cas, on retire des colonnes tant que la rangee ne tient pas a 44 px (JAMAIS de debordement horizontal).
 */
function resoudreRangee(largeur: number, a: ZoneEtat, b: ZoneEtat): [ZoneEtat, ZoneEtat] {
  const largeurOk = (seuil: number) => dPourRangee(largeur, a, b) >= seuil
  const reduire = (seuil: number, queAuto: boolean): boolean => {
    // retire une colonne a la zone qui en a le plus (a egalite : la seconde), parmi celles autorisees
    const candidates = [a, b].filter((z) => z.colonnes > 1 && (!queAuto || z.auto))
    if (candidates.length === 0) return false
    candidates.sort((x, y) => y.colonnes - x.colonnes)
    candidates[0]!.colonnes -= 1
    void seuil
    return true
  }
  while (!largeurOk(D_AUTO_MIN) && reduire(D_AUTO_MIN, true)) {
    /* l'Auto cede d'abord */
  }
  while (!largeurOk(D_MIN) && reduire(D_MIN, false)) {
    /* puis, si meme a 44 px la rangee deborde, on retire des colonnes choisies */
  }
  return [a, b]
}

export function calculerDisposition(entree: Entree): Disposition {
  const { largeur, hauteur } = entree
  const etats = RANGEES.map(([gc, dc]) => resoudreRangee(largeur, zoneEtat(gc, entree), zoneEtat(dc, entree)))

  // 1. le diametre permis par la largeur (le plus petit des trois rangees), plafonne a D_MAX
  const dLargeur = Math.max(D_MIN, Math.min(D_MAX, Math.floor(Math.min(...etats.map(([g, dr]) => dPourRangee(largeur, g, dr))))))

  // 2. le plus grand diametre <= dLargeur qui tient en hauteur ; sinon D_MIN (et l'ecran defile)
  const hauteurPour = (d: number): number =>
    BAS_DE_TABLE +
    etats.reduce((somme, [g, dr]) => {
      const hg = hauteurZone(g.cle, g.n, g.colonnes, d)
      const hd = hauteurZone(dr.cle, dr.n, dr.colonnes, d)
      return somme + MARGES_RANGEE + Math.max(hg, hd) + 1
    }, 0)
  let d = dLargeur
  while (d > D_MIN && hauteurPour(d) > hauteur) d -= 1
  const hauteurEstimee = hauteurPour(d)

  // 3. les largeurs : chaque zone prend ce dont elle a besoin, le reste est partage (une zone vide reste un bandeau)
  const rangees = etats.map(([g, dr]) => {
    const place = largeur - 2 * MARGE_RANGEE - SEPARATEUR
    const wg = largeurZone(g.colonnes, coef(g.cle, g.amelios), d)
    const wd = largeurZone(dr.colonnes, coef(dr.cle, dr.amelios), d)
    const reste = Math.max(0, place - wg - wd)
    let lg = wg
    let ld = wd
    if (g.colonnes === 0 && dr.colonnes === 0) {
      lg = place / 2
      ld = place / 2
    } else if (g.colonnes === 0) {
      ld = place - lg
    } else if (dr.colonnes === 0) {
      lg = place - ld
    } else {
      lg += reste / 2
      ld += reste / 2
    }
    const zone = (z: ZoneEtat, w: number): ZoneDisposee => ({
      colonnes: z.colonnes,
      largeur: w,
      largeurColonne: coef(z.cle, z.amelios) * d + 6,
      vide: z.colonnes === 0,
    })
    return { gauche: zone(g, lg), droite: zone(dr, ld) }
  }) as Disposition['rangees']

  return { d, rangees, hauteurEstimee, tient: hauteurEstimee <= hauteur }
}
