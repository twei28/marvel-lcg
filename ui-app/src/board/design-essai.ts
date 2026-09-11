// design-essai.ts — le drapeau du nouveau design (barre, bandeau, assistant).
//
// Deux portes, et rien d'autre : l'URL du plateau (?design=essai l'allume,
// ?design=classique l'éteint, et le choix est mémorisé) et le réglage dans
// Options. Éteint, le plateau est celui d'aujourd'hui : tout le nouveau vit
// sous la classe `design-essai` et la prop `designEssai`.

export const CLE_DESIGN_ESSAI = 'marvel-board-design-essai'

type Stockage = Pick<Storage, 'getItem' | 'setItem'>

export function lireDesignEssai(search: string, stockage: Stockage): boolean {
  const demande = new URLSearchParams(search).get('design')
  if (demande === 'essai' || demande === 'classique') {
    const actif = demande === 'essai'
    try {
      stockage.setItem(CLE_DESIGN_ESSAI, actif ? 'on' : 'off')
    } catch {
      /* préférence non critique */
    }
    return actif
  }
  try {
    return stockage.getItem(CLE_DESIGN_ESSAI) === 'on'
  } catch {
    return false
  }
}
