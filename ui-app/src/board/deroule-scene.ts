// Ce qu'une etape demande a l'ecran.
//
// PUR : aucun DOM, aucune classe CSS. Le hook useDerouleScene applique ces
// decisions ; ici on ne fait que decider. Ce partage rend la regle verifiable
// sans navigateur, et c'est celui de pas-a-pas.ts.

import type { EtapeDeroule } from './deroule-phase'

export type SceneEtape = {
  /** Carte a agrandir, si l'etape en designe une. */
  carteEnAvant?: number
  /** Cible du trait, quand il y en a un. */
  cible?: number
  /** Faut-il tracer le trait de l'auteur vers la cible. */
  trait: boolean
  /** Faut-il assombrir le reste du plateau. */
  voile: boolean
}

const RIEN: SceneEtape = { trait: false, voile: false }

export function sceneDe(etape: EtapeDeroule): SceneEtape {
  if (etape.carteId === undefined) return RIEN

  // Un trait qui part d'une carte pour y revenir ne montre rien.
  const trait = etape.cibleId !== undefined && etape.cibleId !== etape.carteId

  return {
    carteEnAvant: etape.carteId,
    cible: trait ? etape.cibleId : undefined,
    trait,
    voile: true,
  }
}
