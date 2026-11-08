// feuillets.ts — les feuillets de regles propres a un heros (« Feuillet Dazzler », 08/11/2026).
//
// Un feuillet est un PDF d'une page converti en image (feuillets/*.jpg) : l'image est inlinee par Vite
// (assetsInlineLimit) et chargee a l'ouverture de l'onglet seulement, pas dans le paquet du plateau.
// Les feuillets sont en francais : l'onglet disparait quand le joueur est en anglais.
import { langueActuelle } from './langue'

export interface Feuillet {
  /** Prefixe du pic_id de l'identite du heros (`dz` pour dz001a). */
  prefixe: string
  titre: string
  charger: () => Promise<string>
}

export const FEUILLETS: readonly Feuillet[] = [
  { prefixe: 'dz', titre: 'Dazzler', charger: async () => (await import('./feuillets/dazzler.jpg')).default },
]

/** Les feuillets des heros presents dans la partie, sans doublon, dans l'ordre du registre. Vide en anglais. */
export function feuilletsDeLaPartie(picIdsHeros: readonly (string | undefined)[]): Feuillet[] {
  if (langueActuelle() !== 'fr') return []
  return FEUILLETS.filter((f) => picIdsHeros.some((id) => id && new RegExp(`^${f.prefixe}\\d{3}`).test(id)))
}
