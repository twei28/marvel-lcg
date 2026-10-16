// « Étape par étape bis » (16/10/2026) : la NOUVELLE phase du méchant, offerte
// aux seuls comptes qui ont l'essai (coché par compte dans /admin, voir
// essais.ts `essaiPhaseMechant`). Ces comptes choisissent, dans les Réglages,
// entre « Étape par étape » (la présentation de tout le monde) et « Étape par
// étape bis » (la nouvelle). Les autres comptes ne voient rien de neuf.
//
// Le choix vit dans le navigateur ; « bis » par défaut, pour qu'un compte qui
// avait l'essai le garde tel qu'il le connaissait.

export const CLE_PHASE_BIS = 'mc_phase_bis'
const EVENEMENT = 'mc-phase-bis'

export function lirePhaseBis(): boolean {
  try {
    return globalThis.localStorage?.getItem(CLE_PHASE_BIS) !== 'non'
  } catch {
    return true
  }
}

export function ecrirePhaseBis(oui: boolean): void {
  try {
    globalThis.localStorage?.setItem(CLE_PHASE_BIS, oui ? 'oui' : 'non')
  } catch {
    /* stockage refuse : le choix vaudra pour la page */
  }
  globalThis.dispatchEvent?.(new CustomEvent(EVENEMENT, { detail: oui }))
}

/** Suit le choix (Réglages ouverts dans la même page). Rend de quoi se désabonner. */
export function suivrePhaseBis(rappel: (oui: boolean) => void): () => void {
  const ecoute = (e: Event) => rappel(Boolean((e as CustomEvent).detail))
  globalThis.addEventListener?.(EVENEMENT, ecoute)
  return () => globalThis.removeEventListener?.(EVENEMENT, ecoute)
}
