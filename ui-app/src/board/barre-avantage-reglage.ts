// LA BARRE D'AVANTAGE : l'interrupteur (22/10/2026). Une option, DESACTIVEE par defaut (decision de l'utilisateur) :
// elle vit dans Reglages, Apparence, et se retient dans le navigateur. Un evenement previent la barre quand on
// bascule, pour qu'elle apparaisse ou disparaisse sans recharger la page.

export const CLE_BARRE_AVANTAGE = 'mc_barre_avantage'
export const EVENEMENT_BARRE_AVANTAGE = 'mc-barre-avantage'

export function lireBarreAvantage(): boolean {
  try {
    return window.localStorage.getItem(CLE_BARRE_AVANTAGE) === 'oui'
  } catch {
    return false
  }
}

export function ecrireBarreAvantage(actif: boolean): void {
  try {
    window.localStorage.setItem(CLE_BARRE_AVANTAGE, actif ? 'oui' : 'non')
  } catch {
    /* stockage indisponible : le choix vaut jusqu'au rechargement */
  }
  window.dispatchEvent(new Event(EVENEMENT_BARRE_AVANTAGE))
}
