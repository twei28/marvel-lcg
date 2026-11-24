// Disposition de la table en RONDS, version « grilles par zone » (27/10/2026, maquette approuvee dispo-ronds.html).
//
// Chaque zone a une GRILLE propre (un nombre fixe de colonnes et de lignes de ronds visibles) :
//   - Mechant, Manigances, Allies, Sbires : 2 colonnes x 2 lignes (4 ronds visibles au plus) ;
//   - Heros : 1 x 1 (un seul rond) ;
//   - Cartes en jeu : 3 colonnes x 2 lignes (6 ronds visibles au plus).
//
// Les ronds sont de taille FIXE (le CSS pose `--d` d'apres la largeur de l'ecran, jamais d'apres le nombre de ronds).
// Les ronds se remplissent LIGNE par ligne (cote a cote), puis, au-dela de la grille visible, en colonnes ajoutees a
// droite (remplies de haut en bas) : voir `enColonnes`. Si une zone a plus de colonnes que sa grille n'en montre, une
// paire de fleches ◂ ▸ la fait defiler d'UNE colonne a la fois (pagination independante par zone). Une zone vide est
// masquee ; si les deux zones d'une rangee sont vides, la rangee disparait.
//
// Fonction PURE et sans DOM : elle part des ronds d'une zone et de sa page courante, et rend les colonnes visibles et
// l'etat des fleches. `TableRonds` garde la page de chaque zone et appelle `disposerZone` au rendu.
import type { CleZone } from './repartir-ronds'

/** La grille visible d'une zone : `cols` colonnes de `rows` ronds. */
export type GrilleZone = { cols: number; rows: number }

/** Les grilles approuvees (maquette dispo-ronds.html). */
export const GRILLES: Record<CleZone, GrilleZone> = {
  vilain: { cols: 2, rows: 2 },
  manigances: { cols: 2, rows: 2 },
  allies: { cols: 2, rows: 2 },
  sbires: { cols: 2, rows: 2 },
  heros: { cols: 1, rows: 1 },
  enJeu: { cols: 3, rows: 2 },
}

/** Les rangees : deux zones cote a cote. Mechant | Manigances, Allies | Sbires, Heros | Cartes en jeu. */
export const RANGEES: ReadonlyArray<readonly [CleZone, CleZone]> = [
  ['vilain', 'manigances'],
  ['allies', 'sbires'],
  ['heros', 'enJeu'],
]

/**
 * Range `items` en COLONNES, exactement comme la maquette (`enColonnes`) :
 *  - les `cols × rows` premiers ronds remplissent la grille LIGNE par ligne (ligne 0 de gauche a droite, puis ligne 1...) ;
 *  - les ronds en surplus ajoutent des colonnes a DROITE, remplies de haut en bas (`rows` par colonne).
 * Les colonnes vides (il n'y a pas assez de ronds pour elles) sont ensuite retirees par `disposerZone`.
 */
export function enColonnes<T>(items: readonly T[], cols: number, rows: number): T[][] {
  const colonnes: T[][] = Array.from({ length: cols }, () => [])
  const premier = cols * rows
  for (let i = 0; i < items.length; i++) {
    if (i < premier) {
      const r = Math.floor(i / cols)
      const c = i % cols
      colonnes[c]![r] = items[i]!
    } else {
      const o = i - premier
      const cc = cols + Math.floor(o / rows)
      const rr = o % rows
      ;(colonnes[cc] ??= [])[rr] = items[i]!
    }
  }
  return colonnes
}

export type ZoneDisposee<T> = {
  /** Les colonnes VISIBLES (celles de la fenetre courante), chacune une pile de ronds (taille <= `rows`). */
  colonnes: T[][]
  /** Le nombre total de colonnes NON VIDES de la zone (sert aux fleches). */
  total: number
  /** La page (decalage en colonnes) effectivement appliquee, bornee a `[0, total - cols]`. */
  page: number
  /** La grille de la zone. */
  grille: GrilleZone
  /** Une paire de fleches est necessaire : il y a plus de colonnes que la grille n'en montre. */
  fleches: boolean
  /** Il reste des colonnes a gauche / a droite de la fenetre. */
  peutReculer: boolean
  peutAvancer: boolean
}

/**
 * La disposition d'UNE zone : ses colonnes visibles et l'etat des fleches, pour une page donnee.
 * `items` : les ronds de la zone (y compris d'eventuels fantomes « vaincu », places a la fin comme des ronds ordinaires).
 */
export function disposerZone<T>(cle: CleZone, items: readonly T[], page: number): ZoneDisposee<T> {
  const grille = GRILLES[cle]
  const colonnes = enColonnes(items, grille.cols, grille.rows).filter((c) => c.length > 0)
  const total = colonnes.length
  const maxPage = Math.max(0, total - grille.cols)
  const pageBornee = Math.min(Math.max(0, page), maxPage)
  return {
    colonnes: colonnes.slice(pageBornee, pageBornee + grille.cols),
    total,
    page: pageBornee,
    grille,
    fleches: total > grille.cols,
    peutReculer: pageBornee > 0,
    peutAvancer: pageBornee < maxPage,
  }
}

// -------------------------------------------------------------------------------------------------------------------
// Compatibilite : le reglage « Colonnes par zone » (FenetreReglages, reglages-telephone) existe encore comme preference
// de l'appareil, mais la disposition en grilles fixes ci-dessus ne s'en sert plus. On garde ses types et son defaut pour
// que ces fichiers continuent de compiler (ils seront nettoyes a part, hors du perimetre « ronds »).
export type NbColonnes = 0 | 1 | 2 | 3 | 4
export type ColonnesZones = { manigances: NbColonnes; allies: NbColonnes; sbires: NbColonnes; enJeu: NbColonnes }
export const COLONNES_PAR_DEFAUT: ColonnesZones = { manigances: 3, allies: 3, sbires: 3, enJeu: 4 }
