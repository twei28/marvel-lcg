// Le tirage « au hasard » fait PAR LE JOUEUR (14/11/2026, rapport 131 : « Capturé par Hydra », « Défausse 1 carte
// au hasard »). Quand la règle de partie `tirage_manuel` est cochée, le moteur ne tire pas : il pose la question
// `Player.AskPickHiddenCard` (player_ask.py), dont chaque option porte ce préfixe devant son rang. Le plateau y
// reconnaît « des dos de cartes à mélanger » et non une liste de noms.
// ⚠ Même constante que `Player.PREFIXE_TIRAGE_CACHE` côté moteur.
import type { Option } from './ask'

export const PREFIXE_TIRAGE_CACHE = '[tirage-cache] '
/** Durée du mélange avant que les dos soient cliquables (demande du 14/11/2026 : une seconde). */
export const DUREE_MELANGE_MS = 1000

export function estOptionTirageCache(option: Pick<Option, 'name'>): boolean {
  return typeof option.name === 'string' && option.name.startsWith(PREFIXE_TIRAGE_CACHE)
}

/** Toutes les options sont des dos à tirer (et il y en a au moins deux). */
export function estTirageCache(options: readonly Pick<Option, 'name'>[]): boolean {
  return options.length > 1 && options.every(estOptionTirageCache)
}
