// Le choix des DOS DE CARTES (12/10/2026) : les dos officiels Marvel, ou ceux
// de NarwhalChampions (assets/textures/<camp>-narwhal.webp). Officiels par
// défaut ; posé dans la fenêtre de bienvenue de la préparation, modifiable dans
// les réglages du plateau. La clé est lue aussi par la préparation (même nom).

export type DosCartes = 'officiels' | 'narwhal'

export const CLE_DOS_CARTES = 'marvel-board-dos-cartes'

const DOS_GENERIQUES: ReadonlySet<string> = new Set(['player', 'encounter', 'villain'])

export function lireDosCartes(): DosCartes {
  try {
    return window.localStorage.getItem(CLE_DOS_CARTES) === 'narwhal' ? 'narwhal' : 'officiels'
  } catch {
    return 'officiels'
  }
}

export function ecrireDosCartes(choix: DosCartes): void {
  try {
    window.localStorage.setItem(CLE_DOS_CARTES, choix)
  } catch {
    /* preference non critique : le choix vaut pour la session */
  }
}

export function estDosGenerique(picId: string): boolean {
  return DOS_GENERIQUES.has(picId)
}

/** Le nom d'image d'un dos générique selon le choix du joueur. */
export function dosPicId(picId: string, choix: DosCartes = lireDosCartes()): string {
  if (!estDosGenerique(picId)) return picId
  return choix === 'narwhal' ? `${picId}-narwhal` : picId
}
