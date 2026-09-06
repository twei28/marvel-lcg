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
  if (etape.carteId === undefined) {
    // Sans auteur NI cible, il n'y a rien a montrer : le cartouche parle seul
    // et l'ecran ne bouge pas pour rien.
    if (etape.cibleId === undefined) return RIEN
    // Une cible sans auteur : l'etape de menace, ou c'est une regle du jeu qui
    // pose la menace, pas un personnage. On met alors la CIBLE en avant, faute
    // d'auteur, et on assombrit le reste comme partout ailleurs. Aucun trait :
    // il faut deux cartes pour en tracer un, et une fleche partant de nulle
    // part ne montrerait rien.
    return { carteEnAvant: etape.cibleId, trait: false, voile: true }
  }

  // Un trait qui part d'une carte pour y revenir ne montre rien.
  const trait = etape.cibleId !== undefined && etape.cibleId !== etape.carteId

  return {
    carteEnAvant: etape.carteId,
    cible: trait ? etape.cibleId : undefined,
    trait,
    voile: true,
  }
}
