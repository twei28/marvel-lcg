// design-essai.ts — le drapeau du nouveau design (barre, bandeau, assistant).
//
// ⚠ IL EST LE DEFAUT depuis le 11/09/2026, apres essai (decision de
// l'utilisateur). C'est donc l'ANCIEN plateau qu'il faut demander maintenant :
// ?design=classique dans l'URL, ou la ligne dans Options. Le choix est
// mémorisé par navigateur, comme les animations et les sons — et, comme elles,
// seule la valeur « off » compte : un stockage vide ou refusé laisse le
// nouveau design.
//
// Tout le nouveau vit sous la classe `design-essai` et la prop `designEssai` :
// l'ancien rendu reste intact derrière, à l'octet près.

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
    return stockage.getItem(CLE_DESIGN_ESSAI) !== 'off'
  } catch {
    return true
  }
}
