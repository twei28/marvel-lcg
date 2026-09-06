// Une partie a plusieurs heros sur UN ecran tient tous les sieges a la fois :
// le socket s'ouvre avec `hot_seat`, et le moteur rend la liste des sieges
// d'apres `controller_manager.total_players`.
//
// ⚠ CE COMPTE VAUT ZERO TANT QUE LA PARTIE N'EST PAS MONTEE
// (engine/controller/manager.py). Le site redirige vers le plateau des que le
// port du moteur repond, donc AVANT la mise en place : le socket s'ouvrait sur
// une liste de sieges vide et le client n'en tenait aucun.
//
// Ce qui rend la panne silencieuse : le moteur n'envoie ses trames qu'aux
// clients D'UN SIEGE (`WebSendRender(player_id)` -> `GetClients`). Sans siege,
// on ne recoit donc RIEN — pas d'erreur, pas de fermeture, juste un socket
// ouvert et muet. La main n'arrivait qu'au premier changement de phase, quand le
// moteur rouvre les sieges qu'il croit abandonnes. D'ou la trentaine de secondes
// signalee en jeu.
//
// Le signal a guetter est donc le SILENCE, pas un message. En local le defaut ne
// se voit pas : on ouvre le navigateur a la main, bien apres le demarrage.

/** Delai laisse au moteur pour envoyer sa premiere trame, en millisecondes. */
export const DELAI_PREMIERE_TRAME_MS = 3000

/**
 * Le socket est ouvert mais muet : faut-il le rouvrir pour reclamer les sieges ?
 *
 * Une seule fois. Rouvrir en boucle empecherait la partie de demarrer, et un
 * moteur simplement lent finirait par repondre.
 */
export function doitRattraperLesSieges({
  multijoueur,
  trameRecue,
  dejaRattrape,
}: {
  /** Partie REPARTIE sur plusieurs machines : chacun tient son siege, on ne touche a rien. */
  multijoueur: boolean
  /** A-t-on recu au moins une trame depuis l'ouverture ? */
  trameRecue: boolean
  dejaRattrape: boolean
}): boolean {
  if (multijoueur || dejaRattrape) return false
  return !trameRecue
}
