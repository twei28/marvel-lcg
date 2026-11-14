// reglages-divers.ts — les quelques preferences qui vivaient, jusqu'au
// 06/11/2026, comme de simples constantes/fonctions LOCALES a board.tsx
// (animations, sons, revelation, mode d'actions). Sorties ici pour la meme
// raison que teinte.ts ou scans-fr.ts : la fenetre des Reglages, ouverte
// depuis l'accueil (avant toute partie, tuile Options), doit lire et ecrire
// EXACTEMENT les memes cles que le plateau. board.tsx garde la glue React
// (useState/useCallback) ; ce module ne porte que la lecture/ecriture pure.
import type { ModeActions, ModeRevelation } from './moteur'

export const CLE_MODE_ACTIONS = 'marvel-board-action-mode'

export function lireModeActions(): ModeActions {
  try {
    return window.localStorage.getItem(CLE_MODE_ACTIONS) === 'detailed' ? 'detailed' : 'simple'
  } catch {
    return 'simple'
  }
}

export const CLE_ANIMATIONS = 'marvel-board-animations'

/** Animations de deplacement activees ? Par defaut oui, sauf choix contraire. */
export function lireAnimations(): boolean {
  try {
    return window.localStorage.getItem(CLE_ANIMATIONS) !== 'off'
  } catch {
    return true
  }
}

export const CLE_SONS = 'marvel-board-sons'

/** Sons du moteur actifs ? Par defaut oui, comme le client d'origine. */
export function lireSons(): boolean {
  try {
    return window.localStorage.getItem(CLE_SONS) !== 'off'
  } catch {
    return true
  }
}

export const CLE_REVELATION = 'marvel-board-revelation'

export const DUREES_REVELATION: Record<ModeRevelation, number> = { off: 0, court: 2600, long: 5000 }

export function lireRevelation(): ModeRevelation {
  try {
    const valeur = window.localStorage.getItem(CLE_REVELATION)
    return valeur === 'off' || valeur === 'long' ? valeur : 'court'
  } catch {
    return 'court'
  }
}
