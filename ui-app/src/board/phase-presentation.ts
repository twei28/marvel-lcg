// La PRÉSENTATION de la phase du méchant, parmi les trois qui partagent le rythme
// « Étape par étape » (mode `detaille`, voir moteur.ts) : 16/10/2026.
//
//  - `etape`      : « Étape par étape », le cartouche d'origine, au centre ;
//  - `bis`        : « Étape par étape bis », la nouvelle phase du méchant (essai) ;
//  - `dynamique`  : « Phase dynamique », la quatrième présentation (essai) : le même
//                   cartouche détaillé, posé en panneau à DROITE de la table, la
//                   table restant jouable (cartouche-dynamique.css).
//
// ⚠ CE N'EST PAS UN MODE DU MOTEUR. `ModePhaseMechant` ne bouge pas (`detaille`,
// `sur-table`, `instantane`) : la présentation ne change que la mise en scène, le
// moteur retient et relâche ses trames exactement de la même façon. Les comptes
// qui n'ont pas l'essai (`essais.ts`) ne voient jamais que `etape`.
//
// Le choix vit dans le navigateur. Il remplace `mc_phase_bis` (oui/non, du matin du
// 16/10/2026), toujours lu s'il n'y a pas encore de choix : `non` donne `etape`,
// tout le reste donne `bis`, le défaut d'alors. Aucun réglage n'est perdu.

export type PresentationPhase = 'etape' | 'bis' | 'dynamique'

export const PRESENTATIONS: readonly PresentationPhase[] = ['etape', 'bis', 'dynamique']

export const CLE_PRESENTATION_PHASE = 'mc_phase_presentation'
const CLE_ANCIENNE_PHASE_BIS = 'mc_phase_bis'
const EVENEMENT = 'mc-phase-presentation'

export function lirePresentationPhase(): PresentationPhase {
  try {
    const stocke = globalThis.localStorage?.getItem(CLE_PRESENTATION_PHASE)
    if (stocke && (PRESENTATIONS as readonly string[]).includes(stocke)) return stocke as PresentationPhase
    return globalThis.localStorage?.getItem(CLE_ANCIENNE_PHASE_BIS) === 'non' ? 'etape' : 'bis'
  } catch {
    return 'bis'
  }
}

export function ecrirePresentationPhase(presentation: PresentationPhase): void {
  try {
    globalThis.localStorage?.setItem(CLE_PRESENTATION_PHASE, presentation)
  } catch {
    /* stockage refuse : le choix vaudra pour la page */
  }
  globalThis.dispatchEvent?.(new CustomEvent(EVENEMENT, { detail: presentation }))
}

/** Suit le choix (Réglages ouverts dans la même page). Rend de quoi se désabonner. */
export function suivrePresentationPhase(rappel: (presentation: PresentationPhase) => void): () => void {
  const ecoute = (e: Event) => rappel((e as CustomEvent<PresentationPhase>).detail)
  globalThis.addEventListener?.(EVENEMENT, ecoute)
  return () => globalThis.removeEventListener?.(EVENEMENT, ecoute)
}
