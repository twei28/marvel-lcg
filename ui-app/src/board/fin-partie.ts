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

/**
 * Le temps au bout duquel l'écran de fin s'affiche QUOI QU'IL ARRIVE.
 *
 * Le coup fatal se voit avant l'écran de fin (décision de conception : « on
 * comprend ce qui nous a tués »), mais rien ne doit pouvoir empêcher cet écran
 * de paraître — un joueur qui s'éloigne, un cartouche resté sur une étape qu'il
 * ne sait plus valider. Vingt secondes : le temps de lire une étape de
 * cartouche trois fois, jamais celui de croire que la partie est bloquée.
 */
export const DELAI_FILET_FIN_PARTIE_MS = 20_000

/**
 * Une étape du déroulé porte-t-elle la chute du héros de CE siège ?
 *
 * `defaite` est déjà posée par `etapesDeroule`, qui croise le compteur du fait
 * et les héros que le monde déclare éliminés (voir `EtapeDeroule.defaite`) :
 * on ne la recalcule pas. On ne fait que trancher si c'est NOTRE héros, parce
 * que la défaite d'un autre joueur ne retient l'écran de fin de personne
 * d'autre que lui.
 *
 * `herosLocauxIds` porte les deux faces (héros et alter ego) : un héros peut
 * tomber sous l'une comme sous l'autre.
 */
export function coupFatalLocal(
  etapes: { defaite?: boolean; cibleId?: number }[],
  herosLocauxIds: Set<number>
): boolean {
  return etapes.some(
    (etape) => etape.defaite && etape.cibleId !== undefined && herosLocauxIds.has(etape.cibleId)
  )
}

/**
 * L'écran de fin de partie doit-il s'afficher MAINTENANT ?
 *
 * `partieFinie` (`monde.game_over`) reste la seule source de la fin de partie ;
 * cette fonction ne fait que la RETARDER, et seulement dans un cas : le déroulé
 * détaillé a une étape de coup fatal à montrer et le joueur ne l'a pas encore
 * validée. Le code faisait l'inverse : le cartouche disparaissait à la trame
 * même où l'écran de fin paraissait, et le joueur ne voyait jamais l'étape qui
 * l'avait tué (constat M5 de l'audit du 06/09/2026).
 *
 * Deux sorties de secours, et c'est voulu : le filet de temps (`filetEcoule`)
 * et l'absence de coup fatal local. Toute incertitude penche du côté de
 * l'affichage : un écran de fin en avance vaut mieux qu'un écran qui ne vient
 * jamais.
 */
export function afficherFinDePartie({
  partieFinie,
  coupFatalAMontrer,
  coupFatalVu,
  filetEcoule,
}: {
  partieFinie: boolean
  coupFatalAMontrer: boolean
  coupFatalVu: boolean
  filetEcoule: boolean
}): boolean {
  if (!partieFinie) return false
  if (!coupFatalAMontrer) return true
  return coupFatalVu || filetEcoule
}
