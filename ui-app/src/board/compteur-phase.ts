// compteur-phase.ts : le mode de la phase du mechant choisi, remonte UNE FOIS par partie (Play seulement) au compteur
// anonyme du site (`/compteur_phase_play`). Aucun identifiant : une valeur d'une liste fermee, rien d'autre.
// Jamais bloquant : tout echec est avale.

import type { ModePhaseMechant } from './moteur'
import type { PresentationPhase } from './phase-presentation'

export type ValeurCompteurPhase = 'guidee' | 'plateau_anime' | 'accelere' | 'etape' | 'telephone'

/**
 * La valeur EFFECTIVE : sur telephone le mode est force (« Guidee » d'office), on le compte a part (`telephone`) pour
 * ne pas gonfler « guidee ». Sinon : `sur-table` = Plateau anime, `instantane` = Accelere, `detaille` = Guidee (`tris`)
 * ou l'ancien « Etape par etape » (toute autre presentation, mode cache).
 */
export function valeurCompteurPhase(
  mode: ModePhaseMechant,
  presentation: PresentationPhase,
  telephone: boolean,
): ValeurCompteurPhase {
  if (telephone) return 'telephone'
  if (mode === 'sur-table') return 'plateau_anime'
  if (mode === 'instantane') return 'accelere'
  return presentation === 'tris' ? 'guidee' : 'etape'
}

/** L'adresse du compteur sur le site principal, ou null hors `play.*` (rien n'est compte ailleurs). */
export function adresseCompteurPhase(origine: string, hote: string): string | null {
  if (!hote.startsWith('play.')) return null
  return origine.replace('//play.', '//') + '/compteur_phase_play'
}

let dejaSignale = false

/** Remet le garde a zero (tests). */
export function reinitialiserCompteurPhase(): void {
  dejaSignale = false
}

/** Envoie la valeur, une seule fois par chargement du plateau. Rend vrai si un envoi a ete tente. */
export function signalerModePhase(
  valeur: ValeurCompteurPhase,
  lieu: { origin: string; hostname: string } = globalThis.location,
  envoyer: ((url: string, corps: string) => unknown) | undefined = globalThis.navigator?.sendBeacon?.bind(globalThis.navigator),
): boolean {
  if (dejaSignale) return false
  try {
    const url = adresseCompteurPhase(lieu.origin, lieu.hostname)
    if (!url || !envoyer) return false
    dejaSignale = true
    envoyer(url, JSON.stringify({ phase: valeur }))
    return true
  } catch {
    return false
  }
}
