// Jusqu'ou la vue « Auto » a le droit de suivre celui qui doit agir.
//
// Elle suit le joueur que le moteur interroge, ce qui est juste tant qu'on peut
// voir ce qu'il se passe chez lui. Pendant les mulligans, le moteur s'adresse a
// chaque joueur a son tour : la vue partait alors chez le voisin, dont la main
// nous est CACHEE (le moteur ne la montre qu'au siege qui la tient). On se
// retrouvait devant son plateau, sans main et sans rien a faire — indiscernable
// d'une partie bloquee, et signale comme tel.

import { isVisibleFor, type World } from './world'

/**
 * A-t-on quelque chose a voir chez ce joueur ?
 *
 * Oui pour notre propre siege, evidemment. Oui aussi pour un voisin dont la main
 * nous est visible : c'est le cas du hot-seat, un seul navigateur pour tous les
 * sieges, ou le suivi automatique garde tout son sens. Oui encore s'il n'a pas
 * de main du tout — rien n'est cache, donc rien ne manquera a l'ecran.
 *
 * Non, en revanche, quand il tient des cartes que le moteur nous refuse.
 */
export function peutSuivre(
  monde: World | undefined,
  cible: number,
  playerId: number
): boolean {
  // Premier rendu : rien n'est charge, on ne bloque pas le suivi.
  if (!monde) return true
  if (cible === playerId) return true

  const joueurs = Array.isArray(monde.players) ? monde.players : []
  const joueur = joueurs[cible]
  if (!joueur) return false

  const main = Array.isArray(joueur.hand_cards) ? joueur.hand_cards : []
  if (main.length === 0) return true

  return main.some((carte) => isVisibleFor(carte, playerId))
}
