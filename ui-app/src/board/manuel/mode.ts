// mode.ts — la reconnaissance du mode manuel, en un seul endroit.
//
// Le mode manuel N'EST PAS le bac à sable, même si les deux partagent le menu
// d'intervention : le bac à sable est une partie normale qu'on truque, le mode
// manuel est une table où le moteur ne joue plus. Les confondre ferait taire le
// plateau d'une partie qui se joue encore aux règles.
import type { World } from '../world'

export function estModeManuel(world: World | undefined): boolean {
  return world?.mode_manuel === true
}

/**
 * Le moteur s'est-il tu (tâche 8 bis) ?
 *
 * DISTINCT de `estModeManuel` : celle-ci lit la RÈGLE (vraie dès la création
 * de la partie, mise en place comprise), celle-ci lit l'ÉTAT (vrai seulement
 * une fois la boucle manuelle entrée, `World.ManualLoop` côté moteur).
 *
 * C'est CETTE fonction que tout masquage d'une couche du moteur (bandeau de
 * phase, demande centrale, assistant d'action...) et tout geste manuel
 * (menu, clavier, glisser) doit interroger. Se régler sur `estModeManuel`
 * masquerait le panneau de mulligan PENDANT la mise en place — la partie
 * resterait bloquée pour toujours, le moteur attendant une réponse qu'aucune
 * couche ne permettrait plus de donner.
 */
export function leMoteurSeTait(world: World | undefined): boolean {
  return world?.manuel_actif === true
}

/**
 * Une partie ORDINAIRE est-elle en pause manuelle EN COURS DE PARTIE (tâche 3) ?
 *
 * DISTINCT de `leMoteurSeTait` tout seul : une partie DÉCLARÉE manuelle porte
 * elle aussi `manuel_actif` à vrai en permanence une fois la mise en place
 * terminée (`World.ManualLoop`, côté moteur, n'est entrée QUE si
 * `rule.mode_manuel` est vraie, `game/world/world.py:1030`) — ce n'est pas
 * une PAUSE, c'est la NATURE de la partie, et il n'y a rien à « reprendre ».
 * Une pause ad hoc (route `POST /manuel_pause`), elle, ne peut survenir QUE
 * sur une partie qui n'a jamais déclaré `mode_manuel` — sans quoi
 * `World.ManualLoop` aurait déjà pris la main pour de bon.
 *
 * C'est CETTE fonction qui doit armer le bandeau de pause (`BandeauPause`) et
 * le bouton qui le déclenche dans la barre du haut : se régler sur
 * `leMoteurSeTait` seul afficherait « Partie en pause / Reprendre » sur une
 * table manuelle déclarée qui n'a jamais été mise en pause et n'a rien à
 * reprendre.
 */
export function estEnPause(world: World | undefined): boolean {
  return leMoteurSeTait(world) && !estModeManuel(world)
}
