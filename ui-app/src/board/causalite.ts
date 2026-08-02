// Rattacher une cause aux entrees chiffrees de l'historique.
//
// L'historique se construit en comparant deux instantanes du monde. Un diff
// voit qu'un total de PV ou de menace a bouge ; il ne peut pas savoir POURQUOI.
// D'ou des lignes muettes du genre « Quasar takes 1 damage », qui obligent a
// reconstruire l'enchainement de tete.
//
// La cause existe pourtant deja : le moteur la narre une ou deux passes plus
// tot, avec l'auteur ET la carte responsable.
//
//   Quasar would deal 2 damage to Evil Gwenpool (Quasar)
//   Evil Gwenpool will take 2 damage from Quasar (Quasar)
//   Underground Distribution would place 2⚠ (Main Scheme Phase Place Threat)
//
// Le « ({effet}) » de fin de ligne est le `by_effect.this` du moteur : la carte
// ou la regle qui declenche. C'est le « via quoi ».
//
// Gabarits repris de src/game/message/sender/sender_damage.py (lignes 325, 611,
// 739) et sender_scheme.py (ligne 85). La narration arrive en anglais ; si elle
// venait a etre traduite, les motifs cesseraient simplement de matcher et
// l'entree perdrait son attribution — elle ne se tromperait pas d'auteur.

import { t } from './langue'

export type GenreCause = 'degats' | 'menace'

export type Cause = {
  genre: GenreCause
  /** Qui encaisse, tel que le moteur ecrit son nom. */
  cible: string
  /** Qui inflige. */
  source?: string
  /** La carte ou la regle responsable : le « ({effect}) » de fin de ligne. */
  via?: string
}

type CauseDatee = Cause & { renderId: number }

export type MemoireCauses = Map<string, CauseDatee>

// Une cause precede son effet d'une poignee de rendus. Au-dela, on prefere ne
// rien afficher plutot que d'attribuer des degats au mauvais coupable.
const PORTEE_RENDUS = 6

/**
 * Un ecart NEGATIF veut dire que le compteur de rendus est reparti en arriere :
 * nouvelle partie, ou retour en arriere. Sans ce test, la soustraction resterait
 * inferieure a la portee et une cause de la partie precedente se recollerait a
 * une carte homonyme.
 */
function estFraiche(renderId: number, causeRenderId: number): boolean {
  const ecart = renderId - causeRenderId
  return ecart >= 0 && ecart <= PORTEE_RENDUS
}

const MOTIFS: Array<[RegExp, (m: RegExpMatchArray) => Cause]> = [
  // « {unit} would deal {damage} damage to {target} ({effect}) »
  [
    /^(.+?) would deal \d+ damage to (.+?)(?: \(([^()]*)\))?$/,
    (m) => ({ genre: 'degats', cible: m[2], source: m[1], via: m[3] }),
  ],
  // « {unit} will take {damage} damage from {source} ({effect}) »
  [
    /^(.+?) will take \d+ damage from (.+?)(?: \(([^()]*)\))?$/,
    (m) => ({ genre: 'degats', cible: m[1], source: m[2], via: m[3] }),
  ],
  // « {trigger} is being attacked by {attacker} » : pas de carte responsable,
  // mais c'est la ligne qui ouvre l'attaque, donc la premiere a donner l'auteur.
  [
    /^(.+?) is being attacked by (.+)$/,
    (m) => ({ genre: 'degats', cible: m[1], source: m[2] }),
  ],
  // « {scheme} would place {value}⚠ ({effect}) » : ici l'auteur EST le « via »,
  // le moteur ne nomme pas de source distincte.
  [
    /^(.+?) would place \d+⚠(?: \(([^()]*)\))?$/,
    (m) => ({ genre: 'menace', cible: m[1], via: m[2] }),
  ],
  // « {unit} will thwart {schemes} ({additional_value:+}) »
  [
    /^(.+?) will thwart (.+?)(?: \([+-]?\d+\))?$/,
    (m) => ({ genre: 'menace', cible: m[2], source: m[1] }),
  ],
]

function cle(genre: GenreCause, cible: string): string {
  return `${genre}:${cible.trim().toLowerCase()}`
}

export function creerMemoireCauses(): MemoireCauses {
  return new Map()
}

/**
 * Lit une ligne de narration deja nettoyee de ses identifiants et retient ce
 * qu'elle dit, s'il s'agit d'une cause.
 */
export function noterCause(memoire: MemoireCauses, texte: string, renderId: number): void {
  for (const [motif, lire] of MOTIFS) {
    const trouve = texte.match(motif)
    if (!trouve) continue

    const cause = lire(trouve)
    const identifiant = cle(cause.genre, cause.cible)
    const precedente = memoire.get(identifiant)

    // Une attaque se narre en plusieurs temps : « is being attacked by » donne
    // l'auteur, « would deal » ajoute la carte responsable. On complete au lieu
    // d'ecraser, mais seulement tant que la precedente est encore fraiche —
    // sinon un ancien « via » se recollerait a une nouvelle attaque.
    const fraiche = precedente !== undefined && estFraiche(renderId, precedente.renderId)
    memoire.set(identifiant, {
      genre: cause.genre,
      cible: cause.cible,
      source: cause.source ?? (fraiche ? precedente.source : undefined),
      via: cause.via ?? (fraiche ? precedente.via : undefined),
      renderId,
    })
    return
  }
}

export function lireCause(
  memoire: MemoireCauses,
  genre: GenreCause,
  cible: string,
  renderId: number
): Cause | undefined {
  const cause = memoire.get(cle(genre, cible))
  if (!cause) return undefined
  if (!estFraiche(renderId, cause.renderId)) return undefined
  if (!cause.source && !cause.via) return undefined
  return cause
}

/**
 * Complete le detail d'une entree (« 2 PV restants ») par son attribution.
 * Quand le moteur repete le meme nom en auteur et en carte responsable — le cas
 * courant d'un allie qui attaque — on ne l'ecrit qu'une fois.
 */
export function detailAvecCause(base: string | undefined, cause: Cause | undefined): string | undefined {
  if (!cause) return base
  const morceaux = base ? [base] : []
  if (cause.source) morceaux.push(`${t('par')} ${cause.source}`)
  if (cause.via && cause.via !== cause.source) morceaux.push(`${t('via')} ${cause.via}`)
  return morceaux.length > 0 ? morceaux.join(' · ') : undefined
}
