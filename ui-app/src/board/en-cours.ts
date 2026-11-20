// en-cours.ts — « Continuer la partie » : ranger la partie dans SON fichier (route `/en_cours_sauver`, voir
// Fusion/marvel-lcg-src/src/engine/en_cours.py).
//
// Retour de testeur du 18/11/2026 : « j'ai joué un allié, je suis retourné au menu, et Continuer me rend d'autres cartes ».
// Cause mesurée : la sauvegarde ne partait qu'au CHANGEMENT de phase, jamais pour la première phase d'une partie. Elle part
// maintenant aussi au retour au menu, à la fermeture de la page et au début de la partie.
//
// ⚠ NE BLOQUE JAMAIS ET N'ÉCHOUE JAMAIS : quitter la partie ne doit pas dépendre d'une sauvegarde. Le moteur refuse seul ce
// qui n'a pas à être rangé (mise en place, partie finie, puzzle).

/** Délai maximal d'attente avant de quitter : au-delà, on part quand même. */
export const ATTENTE_MAX_MS = 1500

/** Range la partie, et rend la main au plus tard après `ATTENTE_MAX_MS`. Silencieux. */
export async function sauverEnCours(attenteMax = ATTENTE_MAX_MS): Promise<void> {
  try {
    await Promise.race([
      fetch('/en_cours_sauver', { cache: 'no-store', keepalive: true }).catch(() => undefined),
      new Promise<void>((fini) => window.setTimeout(fini, attenteMax)),
    ])
  } catch {
    /* jamais bloquant */
  }
}

/** À la fermeture de la page : on lance l'envoi, sans attendre (la page part). `keepalive` le laisse finir. */
export function sauverEnPartant(): void {
  try {
    void fetch('/en_cours_sauver', { cache: 'no-store', keepalive: true }).catch(() => undefined)
  } catch {
    /* jamais bloquant */
  }
}
