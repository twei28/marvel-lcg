// Ce qu'une etape montre dans la scene centrale.
//
// PUR : aucun DOM, aucune classe CSS. DeroulePhase pose les cartes,
// useDerouleScene pose le voile ; ici on ne fait que decider. Ce partage rend
// la regle verifiable sans navigateur, et c'est celui de pas-a-pas.ts.
//
// Une seule regle de taille, decidee avec l'utilisateur le 7 septembre 2026 :
// toutes les cartes de la scene ont la meme taille, face visible. Plus rien
// n'est agrandi sur place dans la table.

import type { EtapeDeroule } from './deroule-phase'

export type CarteDeScene =
  /** Une carte du monde, retrouvee par son identifiant. */
  | { role: 'auteur' | 'cible' | 'boost' | 'revelee'; id: number }
  /**
   * Un dos de carte rencontre : la distribution ne dit pas quelle carte
   * (le moteur ne l'identifie pas, et c'est juste : elle est face cachee).
   */
  | { role: 'dos' }

export type SceneEtape = {
  /** Les cartes, dans l'ordre de gauche a droite. */
  cartes: CarteDeScene[]
  /** Une fleche entre l'auteur (et ses boosts) et la cible. */
  fleche: boolean
  /** Faut-il assombrir la table derriere la scene. */
  voile: boolean
}

const RIEN: SceneEtape = { cartes: [], fleche: false, voile: false }

export function sceneDe(etape: EtapeDeroule): SceneEtape {
  if (etape.temps === 'distribution') {
    const dos = Math.max(1, etape.montant ?? 1)
    return { cartes: Array.from({ length: dos }, () => ({ role: 'dos' })), fleche: false, voile: true }
  }
  // Une ACTIVATION garde sa mise en scene quel que soit son temps. Un vilain
  // qu'une carte revelee fait frapper une seconde fois est range sous
  // « Revelation » (le fait porte sa phase, voir etapesDeroule), mais c'est
  // une attaque : auteur, boosts, fleche, cible. Signale en jeu le 09/09/2026 :
  // la seconde attaque montrait Klaw seul, en retournement de carte revelee,
  // sans cible ni boosts, et « idem pour la manigance ».
  const activation = etape.titre === 'attaque' || etape.titre === 'manigance'
  if (etape.temps === 'revelation' && !activation) {
    if (etape.carteId === undefined) return RIEN
    return { cartes: [{ role: 'revelee', id: etape.carteId }], fleche: false, voile: true }
  }

  const cartes: CarteDeScene[] = []
  if (etape.carteId !== undefined) cartes.push({ role: 'auteur', id: etape.carteId })
  for (const boost of etape.boosts) cartes.push({ role: 'boost', id: boost.cibleId })
  // Un auteur qui est sa propre cible : une seule carte, la fleche n'aurait
  // rien a relier.
  const cible = etape.cibleId !== undefined && etape.cibleId !== etape.carteId
  if (cible && etape.cibleId !== undefined) cartes.push({ role: 'cible', id: etape.cibleId })
  if (cartes.length === 0) return RIEN
  return { cartes, fleche: etape.carteId !== undefined && cible, voile: true }
}
