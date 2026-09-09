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
 * Toujours en hot-seat (un seul navigateur pour tous les sieges). En partie
 * repartie : oui pour notre propre siege, oui pour un voisin dont la main nous
 * est visible, oui encore s'il n'a pas de main du tout — rien n'est cache, donc
 * rien ne manquera a l'ecran.
 *
 * Non, en revanche, quand il tient des cartes que le moteur nous refuse.
 */
export function peutSuivre(
  monde: World | undefined,
  cible: number,
  playerId: number,
  multijoueur: boolean
): boolean {
  // HOT-SEAT : un seul navigateur tient TOUS les sieges, chaque main s'affiche
  // des qu'on regarde son joueur. On suit donc toujours.
  //
  // ⚠ CORRECTIF DU 09/09/2026. La regle testait `visible_for_players` de la
  // main du voisin en croyant qu'en hot-seat le moteur y inscrit tous les
  // sieges locaux. Il n'en est rien : cette liste vient de `IsVisible(player)`
  // (card.py:845), calculee par PROPRIETAIRE et independante du client ; la
  // main du siege 1 y porte [1], jamais [0, 1]. La vue « Auto » ne suivait donc
  // JAMAIS le voisin en hot-seat, et pendant son mulligan on voyait la main du
  // mauvais heros sous la question de l'autre. Signale en jeu a deux heros.
  // En partie repartie, la garde d'origine reste entiere.
  if (!multijoueur) return true
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
