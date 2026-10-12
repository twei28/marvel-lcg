// Les trajets des cartes pendant la phase du méchant (refonte, lot 4, essai,
// 12/10/2026, décisions 49 à 53). Partie PURE : à partir de deux relevés de la
// table (avant / après un changement d'écran), dire quelles cartes arrivent,
// lesquelles partent, et vers quelle pile part chacune.

export type Releve = { id: number; camp?: 'player' | 'encounter' }

export type Changement<R extends Releve = Releve> = { arrivees: number[]; departs: R[] }

/**
 * Au-delà, ce n'est pas un écran qui avance mais la table qui se redessine
 * (début de phase, changement de vue) : on ne fait voler personne.
 */
export const TROP_DE_CHANGEMENTS = 6

export function changementDeTable<R extends Releve>(avant: ReadonlyMap<number, R>, apres: ReadonlyMap<number, R>): Changement<R> {
  const arrivees = [...apres.keys()].filter((id) => !avant.has(id))
  const departs = [...avant.values()].filter((r) => !apres.has(r.id))
  if (arrivees.length + departs.length > TROP_DE_CHANGEMENTS) return { arrivees: [], departs: [] }
  return { arrivees, departs }
}

/** La pile vers laquelle une carte qui quitte la table s'envole (décision 52). */
export function pileDeDepart(camp: Releve['camp']): string {
  return camp === 'encounter' ? '[data-pile$="encounter-discard"]' : '[data-pile$="-defausse"]'
}

/** Durée d'un trajet (décision 53). */
export const DUREE_TRAJET_MS = 600
