// langue.ts — bascule FR/EN de tout le client.
//
// Le français est la langue source du code : t('texte français') renvoie le
// texte tel quel en FR, ou sa version anglaise via DICO_EN quand la langue
// est 'en'. La bascule prévient aussi le moteur (/set_language) pour que la
// narration suive, puis recharge la page : tout se re-rend dans la nouvelle
// langue, et la reconnexion WebSocket est déjà gérée par moteur.ts.

import { DICO_EN_BASE } from './dico-en'

const CLE_LANGUE = 'marvel-langue'

export type Langue = 'fr' | 'en'

export function langueActuelle(): Langue {
  try {
    return localStorage.getItem(CLE_LANGUE) === 'en' ? 'en' : 'fr'
  } catch {
    return 'fr'
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
  try {
    await fetch('/set_language?' + nouvelle)
  } catch {
    /* hors ligne : le client bascule quand même */
  }
  location.reload()
}
