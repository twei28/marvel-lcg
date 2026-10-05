// Le défaut « façon de jouer », partagé avec le lanceur
// (Fusion/marvel-lcg-src/public/js/prepare/facon-de-jouer.js : même clé).
// Il ne change que la case cochée au lancement d'une nouvelle partie.

export type FaconDeJouer = 'auto' | 'manuel'

export const CLE_FACON_DE_JOUER = 'marvel-board-facon-de-jouer'

export function lireFaconParDefaut(): FaconDeJouer {
  try {
    return window.localStorage.getItem(CLE_FACON_DE_JOUER) === 'manuel' ? 'manuel' : 'auto'
  } catch {
    return 'auto'
  }
}

export function ecrireFaconParDefaut(facon: FaconDeJouer): void {
  try {
    window.localStorage.setItem(CLE_FACON_DE_JOUER, facon)
  } catch {
    // stockage bloqué : le défaut ne tient pas, le lanceur reste sur Automatique
  }
}
