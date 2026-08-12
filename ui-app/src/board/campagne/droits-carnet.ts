// Qui écrit quoi dans le carnet, quand la table est répartie sur plusieurs
// appareils.
//
// La règle tient en une phrase : un champ `parJoueur` appartient au siège
// qu'il nomme, tout le reste appartient à l'hôte. Elle vient de la décision du
// 12/8/2026, « chacun ses champs, l'hôte valide ».
//
// Deux conséquences volontaires. L'hôte ne s'approprie PAS les champs
// personnels des autres : s'il le pouvait, deux personnes rempliraient la même
// case et « chacun ses champs » ne voudrait plus rien dire. Et un siège inconnu
// (page ouverte sans `?p=`) ne peut rien écrire du tout.
import type { ChampVictoire } from './detecteurs'

export type DroitCarnet = 'saisie' | 'lecture'

export function droitSurChamp(
  champ: ChampVictoire,
  joueurId: number,
  siege: number,
  estHote: boolean
): DroitCarnet {
  if (siege < 0) return 'lecture'
  if (champ.parJoueur) return joueurId === siege ? 'saisie' : 'lecture'
  return estHote ? 'saisie' : 'lecture'
}

/**
 * Qui termine le scénario pour toute la table.
 *
 * L'hôte, et lui seul. Un distant qui verrait « Valider » reporterait le
 * scénario au carnet depuis un écran où il n'a rempli qu'une case, et les
 * autres perdraient la leur.
 */
export function peutValider(siege: number): boolean {
  return siege === 0
}

/**
 * Cette clé de carnet appartient-elle à un AUTRE siège que le nôtre ?
 *
 * L'hôte recharge la campagne pendant que le panneau est ouvert, pour voir
 * arriver les champs des autres. Il ne doit reprendre que les leurs : une case
 * à lui qu'il vient d'effacer réapparaîtrait à chaque rechargement, et il se
 * battrait contre son propre écran.
 *
 * La forme des clés vient de `cleCarnet()` : « Player <siège + 1> <clé> ». Un
 * champ commun n'a pas de préfixe, et appartient donc à l'hôte. Le numéro est
 * exigé : « Players Rescued » est un champ commun, pas le champ du joueur « s ».
 */
export function cleDUnAutreSiege(cle: string, siege: number): boolean {
  const trouve = /^Player (\d+) /.exec(cle)
  if (!trouve) return false
  return Number(trouve[1]) !== siege + 1
}
