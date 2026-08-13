import type { World } from './world'

/**
 * Ce que l'écran de fin doit annoncer À CE SIÈGE.
 *
 * En partie ordinaire, tout le monde gagne ou perd ensemble : `players_won`
 * suffit. En mode Bataille, la partie se gagne PAR UN CAMP (livret mc56 p.17)
 * et le même écran sert aux deux tables : il faut donc comparer le camp
 * gagnant à celui du siège, sans quoi le vaincu lirait « Victoire ».
 *
 * `teams` est vide hors Bataille : c'est ce qui distingue les deux cas, et
 * aucune partie ordinaire ne change de comportement.
 */
export function finDePartie(
  monde: World,
  siege: number,
): { gagne: boolean; bataille?: { nul: boolean } } {
  const camps = monde.teams ?? []
  if (camps.length === 0) return { gagne: Boolean(monde.players_won) }

  const gagnant = monde.winning_team ?? -1
  const mien = camps[siege] ?? 0
  return { gagne: gagnant >= 0 && gagnant === mien, bataille: { nul: gagnant < 0 } }
}
