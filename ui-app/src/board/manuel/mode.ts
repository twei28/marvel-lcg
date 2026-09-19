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
