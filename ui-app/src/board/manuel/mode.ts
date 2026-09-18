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
