// LE COTE DES AMELIORATIONS (decision du 07/10/2026) : a droite de la carte qui
// les porte (comme toujours), ou a gauche pour qui en a l'habitude. Un seul
// reglage pour toutes les cartes (heros, allies, mechant, sbires), garde dans
// le navigateur. Le placement vit en CSS (board.css, `.est-attachee`) : le
// reglage pose une classe sur <body>, qui inverse le decalage.

export type CoteAmeliorations = 'droite' | 'gauche'

export const CLE_COTE_AMELIORATIONS = 'mc_ameliorations_cote'
export const CLASSE_A_GAUCHE = 'ameliorations-a-gauche'

export function lireCoteAmeliorations(): CoteAmeliorations {
  try {
    return window.localStorage.getItem(CLE_COTE_AMELIORATIONS) === 'gauche' ? 'gauche' : 'droite'
  } catch {
    return 'droite'
  }
}

export function appliquerCoteAmeliorations(cote: CoteAmeliorations): void {
  document.body.classList.toggle(CLASSE_A_GAUCHE, cote === 'gauche')
}

export function ecrireCoteAmeliorations(cote: CoteAmeliorations): void {
  try {
    window.localStorage.setItem(CLE_COTE_AMELIORATIONS, cote)
  } catch {
    /* stockage indisponible : le choix vaut jusqu'au rechargement */
  }
  appliquerCoteAmeliorations(cote)
}
