// LES ETIQUETTES DE TYPE SUR LA TABLE (decision du 07/10/2026) : « ALLIE »,
// « SOUTIEN »... au-dessus des cartes EN JEU n'apprennent rien (la zone et
// l'image le disent deja). Elles restent dans la main, les fenetres et
// l'apercu ; un interrupteur (Reglages, Apparence) les remet sur la table.
// La regle vit en CSS (board.css) : ce module ne pose qu'une classe sur <body>.

export const CLE_ETIQUETTES_TABLE = 'mc_etiquettes_table'
export const CLASSE_ETIQUETTES_TABLE = 'etiquettes-sur-la-table'

export function lireEtiquettesTable(): boolean {
  try {
    return window.localStorage.getItem(CLE_ETIQUETTES_TABLE) === 'oui'
  } catch {
    return false
  }
}

export function appliquerEtiquettesTable(actif: boolean): void {
  document.body.classList.toggle(CLASSE_ETIQUETTES_TABLE, actif)
}

export function ecrireEtiquettesTable(actif: boolean): void {
  try {
    window.localStorage.setItem(CLE_ETIQUETTES_TABLE, actif ? 'oui' : 'non')
  } catch {
    /* stockage indisponible : le choix vaut jusqu'au rechargement */
  }
  appliquerEtiquettesTable(actif)
}
