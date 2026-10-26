// langue.ts — bascule FR/EN de tout le client.
//
// Le français est la langue source du code : t('texte français') renvoie le
// texte tel quel en FR, ou sa version anglaise via DICO_EN quand la langue
// est 'en'. La bascule prévient aussi le moteur (/set_language) pour que la
// narration suive, puis recharge la page : tout se re-rend dans la nouvelle
// langue, et la reconnexion WebSocket est déjà gérée par moteur.ts.

import { DICO_EN_BASE } from './dico-en'
import { cookieLangue, resoudreLangue } from './langue-resolution'
import { alignerScansSurLangue } from './scans-fr'

const CLE_LANGUE = 'marvel-langue'

export type Langue = 'fr' | 'en'

/** La langue du jeu (decision du 26/10/2026) : le choix fait DANS le jeu, sinon le cookie « nc_langue » du site (pose sur le
 *  domaine parent : une table p<N>.<domaine> est une autre origine et ne voit pas le localStorage du site), sinon la langue du
 *  navigateur, sinon le francais. Regle commune : langue-resolution.ts (jumeau de public/js/prepare/langue-resolution.js). */
export function langueActuelle(): Langue {
  let stockage = ''
  try {
    stockage = localStorage.getItem(CLE_LANGUE) || ''
  } catch {
    /* stockage bloque : le cookie et le navigateur decident */
  }
  let cookie = ''
  try {
    cookie = document.cookie
  } catch {
    /* cookies bloques */
  }
  return resoudreLangue({ stockage, cookie, navigateur: typeof navigator === 'undefined' ? null : navigator })
}

/** Le jeu pose AUSSI le cookie « nc_langue » quand le joueur change de langue : le site et les autres tables suivent. */
function poserCookieLangue(langue: Langue): void {
  try {
    document.cookie = cookieLangue(langue, location.host, location.protocol)
  } catch {
    /* cookies bloques */
  }
}

/** Français → anglais. Rempli dans dico-en.ts ; une clé absente reste en FR. */
const DICO_EN: Record<string, string> = { ...DICO_EN_BASE }

export function enregistrerTraductions(entrees: Record<string, string>): void {
  Object.assign(DICO_EN, entrees)
}

export function t(fr: string): string {
  if (langueActuelle() === 'fr') return fr
  return DICO_EN[fr] ?? fr
}

/** Aligne la narration du moteur sur la langue choisie (au chargement). */
export function synchroniserLangueServeur(): void {
  void fetch('/set_language?' + langueActuelle()).catch(() => {})
}

export async function basculerLangue(): Promise<void> {
  const nouvelle: Langue = langueActuelle() === 'fr' ? 'en' : 'fr'
  try {
    localStorage.setItem(CLE_LANGUE, nouvelle)
  } catch {
    /* stockage indisponible : la bascule serveur reste utile */
  }
  poserCookieLangue(nouvelle)
  // Les IMAGES des cartes suivent aussi : elles ont leur propre reglage
  // (« Scans en francais », menu Options), et le laisser en arriere donnait une
  // interface anglaise sur un plateau francais. Le reglage reste modifiable a
  // la main juste apres, pour qui veut le melange.
  alignerScansSurLangue(nouvelle)
  try {
    await fetch('/set_language?' + nouvelle)
  } catch {
    /* hors ligne : le client bascule quand même */
  }
  location.reload()
}
