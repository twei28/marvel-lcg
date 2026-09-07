// Les 12 emplacements de zones.ts, ranges en DEUX rangees de cartes.
//
// C'est une TABLE, pas une logique. Ajouter un emplacement dans zones.ts, c'est
// ajouter une entree ici : le test verifie qu'aucun ne reste orphelin.
//
// Chaque rangee a deux parties : les emplacements qui DEFILENT (les cartes
// posees, de gauche a droite dans l'ordre de lecture) et ceux qui sont
// EPINGLES a droite (les piles : deck et defausse), hors du defilement. La
// main n'est pas une rangee : elle flotte en eventail au-dessus de la barre.
//
// Remplace bandes.ts (modele a medaillons), qui disparait au sous-projet 3.

import { t } from '../langue'
import type { CleEmplacement, EmplacementAffiche, Plateau, UniteAffichee } from '../zones'

export type CleRangee = 'ennemie' | 'heros'

export const RANGEES: Array<{
  cle: CleRangee
  titre: () => string
  defilants: CleEmplacement[]
  epingles: CleEmplacement[]
}> = [
  {
    cle: 'ennemie',
    titre: () => t('Méchant'),
    defilants: ['rencontre', 'complot-principal', 'complots-secondaires', 'terrain-combat'],
    epingles: ['piles-rencontre'],
  },
  {
    cle: 'heros',
    titre: () => t('Ton héros'),
    // La Reserve (pack Brawn) suit le heros, a la meme place que le deck
    // special d'un Doctor Strange : c'est sa zone personnelle.
    defilants: ['terrain-soutien', 'deck-special', 'reserve', 'nemesis'],
    epingles: ['piles-joueur', 'annexes'],
  },
]

export const EMPLACEMENT_MAIN: CleEmplacement = 'main'

export type RangeeAffichee = {
  cle: CleRangee
  titre: string
  defilants: EmplacementAffiche[]
  epingles: EmplacementAffiche[]
}

/** Les deux rangees, TOUJOURS presentes : une rangee vide garde sa place. */
export function repartirEnRangees(plateau: Plateau): RangeeAffichee[] {
  const parCle = new Map<CleEmplacement, EmplacementAffiche>()
  for (const emplacement of plateau.emplacements) parCle.set(emplacement.cle, emplacement)
  const presents = (cles: CleEmplacement[]) =>
    cles
      .map((cle) => parCle.get(cle))
      .filter((emplacement): emplacement is EmplacementAffiche => emplacement !== undefined)

  return RANGEES.map((rangee) => ({
    cle: rangee.cle,
    titre: rangee.titre(),
    defilants: presents(rangee.defilants),
    epingles: presents(rangee.epingles),
  }))
}

/** Toutes les unites de ces emplacements, tous groupes confondus, dans l'ordre. */
export function unitesDe(emplacements: EmplacementAffiche[]): UniteAffichee[] {
  return emplacements.flatMap((emplacement) => emplacement.groupes.flat())
}

export function mainDe(plateau: Plateau): UniteAffichee[] {
  const main = plateau.emplacements.find((emplacement) => emplacement.cle === EMPLACEMENT_MAIN)
  return main ? unitesDe([main]) : []
}

/**
 * `annexes` (zones.ts) porte a la fois des PILES fondues (mises de cote,
 * defausses supplementaires...) et des cartes posees isolees (preuves, regle
 * permanente, ressources) : seules les premieres doivent etre epinglees.
 */
export function estUnePile(unite: UniteAffichee): boolean {
  return unite.pileContenu !== undefined || unite.carte.pileCount !== undefined || unite.pileGroupes !== undefined
}

/** Separe les piles (a epingler) des cartes posees (a rendre dans la rangee qui defile). */
export function separerEpingles(unites: UniteAffichee[]): { piles: UniteAffichee[]; posees: UniteAffichee[] } {
  const piles: UniteAffichee[] = []
  const posees: UniteAffichee[] = []
  for (const uniteCourante of unites) {
    ;(estUnePile(uniteCourante) ? piles : posees).push(uniteCourante)
  }
  return { piles, posees }
}
