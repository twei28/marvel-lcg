// Ce qu'un rendu du moteur change aux STATUTS des personnages.
//
// Signale en jeu le 09/09/2026 : pendant la phase du mechant, les cartes de
// statut (Sonne / Desoriente / Tenace) se posent sans un mot. Le moteur ne
// publie aucun fait « statut » pour le cartouche, la couche d'animations ignore
// volontairement la pile des statuts, et les badges +N / -N ne comparent que
// les compteurs. Le seul signal etait la mini-carte de 50 px sous le porteur.
//
// Ici : on compare, d'un rendu a l'autre, les statuts portes par chaque carte,
// exactement comme `useEffetsCartes` compare la vie et la menace. Pur, sans
// React, pour etre testable tel quel.

import type { WorldCard } from './world'

/**
 * Les statuts du jeu, par `card_id` de leur carte (cards.json, set `status`).
 *
 * `exposed` est le QUATRIEME, ajoute par le pack `sentinel` (T-Wrecks,
 * 12/09/2026) ; `cloaked` le CINQUIEME (pack TMNT, Shredder v3). Sans lui ici, une carte Exposé posée ou retirée ne produirait
 * aucun badge : `estStatut` la rejetterait en silence.
 */
export type Statut = 'stunned' | 'confused' | 'tough' | 'exposed' | 'cloaked'

const STATUTS: readonly Statut[] = ['stunned', 'confused', 'tough', 'exposed', 'cloaked']

function estStatut(valeur: string): valeur is Statut {
  return (STATUTS as readonly string[]).includes(valeur)
}

/**
 * Les statuts portes par chaque carte : porteur -> liste (un statut peut etre
 * double, Steady demande deux Sonne pour mordre).
 *
 * Une carte de statut se reconnait a son type `StatusCard`, et se rattache a
 * son porteur par `bind_object_id` (0 = pas de porteur : la pile de reserve).
 */
export function statutsPortes(cartes: Map<number, WorldCard>): Map<number, Statut[]> {
  const portes = new Map<number, Statut[]>()
  for (const carte of cartes.values()) {
    if (carte.card_type !== 'StatusCard') continue
    if (typeof carte.bind_object_id !== 'number' || carte.bind_object_id === 0) continue
    if (!estStatut(carte.card_id)) continue
    const liste = portes.get(carte.bind_object_id) ?? []
    liste.push(carte.card_id)
    portes.set(carte.bind_object_id, liste)
  }
  return portes
}

export type DeltaStatut = {
  kind: 'status'
  statut: Statut
  /** +1 : le statut vient d'etre pose ; -1 : il vient d'etre retire. */
  value: 1 | -1
}

function compter(liste: Statut[] | undefined): Record<Statut, number> {
  const compte: Record<Statut, number> = { stunned: 0, confused: 0, tough: 0, exposed: 0, cloaked: 0 }
  for (const s of liste ?? []) compte[s] += 1
  return compte
}

/**
 * Pour chaque porteur dont les statuts ont change : ce qui vient d'arriver.
 *
 * Un statut POSE l'emporte sur un statut RETIRE dans le meme rendu (le
 * remplacement d'un Tenace consomme par un nouveau Tenace se lit « Tenace »).
 * Une carte qui n'est plus dans le monde (vaincue) n'a plus de porteur : on ne
 * signale pas la perte de ses statuts, elle est partie avec eux.
 */
export function deltasStatuts(
  avant: Map<number, WorldCard>,
  apres: Map<number, WorldCard>
): Array<[number, DeltaStatut]> {
  const portesAvant = statutsPortes(avant)
  const portesApres = statutsPortes(apres)
  const porteurs = new Set<number>([...portesAvant.keys(), ...portesApres.keys()])
  const deltas: Array<[number, DeltaStatut]> = []
  for (const porteur of porteurs) {
    if (!apres.has(porteur)) continue
    const a = compter(portesAvant.get(porteur))
    const b = compter(portesApres.get(porteur))
    let pose: Statut | undefined
    let retire: Statut | undefined
    for (const s of STATUTS) {
      if (b[s] > a[s]) pose = pose ?? s
      else if (b[s] < a[s]) retire = retire ?? s
    }
    if (pose) deltas.push([porteur, { kind: 'status', statut: pose, value: 1 }])
    else if (retire) deltas.push([porteur, { kind: 'status', statut: retire, value: -1 }])
  }
  return deltas
}

/** Le libelle du badge, dans la langue du plateau. */
export function libelleStatut(statut: Statut, value: 1 | -1, langue: 'fr' | 'en'): string {
  const NOMS: Record<Statut, { fr: string; en: string }> = {
    stunned: { fr: 'Sonné', en: 'Stunned' },
    confused: { fr: 'Désorienté', en: 'Confused' },
    tough: { fr: 'Tenace', en: 'Tough' },
    exposed: { fr: 'Exposé', en: 'Exposed' },
    cloaked: { fr: 'Camouflé', en: 'Cloaked' },
  }
  const nom = NOMS[statut][langue]
  if (value > 0) return nom
  return langue === 'en' ? `${nom} removed` : `${nom} retiré`
}
