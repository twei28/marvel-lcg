import { kindOf } from './card-model'
import { estDefaiteLocale } from './deroule-phase'
import type { World, WorldPlayer } from './world'

/**
 * LES HÉROS QUE CE NAVIGATEUR TIENT, les deux faces de chacun.
 *
 * Hors multijoueur, ce navigateur tient TOUS les sièges : il ouvre son socket
 * en `hot_seat` et répond pour chaque joueur (voir `adresseSocket`, moteur.ts,
 * et la même règle déjà appliquée par `joueurAttendu`). Ne lire que le siège
 * `?p=` était donc faux dès qu'une partie comptait plus d'un héros sur un
 * écran : si le dernier héros à tomber n'était pas celui-là, `coupFatalLocal`
 * rendait faux et le coup fatal n'était JAMAIS montré, l'écran de fin
 * paraissant sur la trame même de `game_over` (le défaut M5, revenu par la
 * porte du hot-seat).
 *
 * En multijoueur, au contraire, chaque navigateur ne tient QUE son siège :
 * la chute du héros d'un autre joueur ne retient l'écran de fin de personne
 * d'autre que lui.
 *
 * `area_hero` porte aussi les améliorations attachées à l'identité : elles ne
 * sont ni héros ni alter ego, d'où le tri sur `kindOf`. Les deux faces
 * comptent, un héros pouvant tomber sous l'une comme sous l'autre.
 */
export function herosLocaux({
  joueurs = [],
  playerId,
  multijoueur,
}: {
  joueurs?: readonly WorldPlayer[]
  playerId: number
  multijoueur: boolean
}): Set<number> {
  const sieges = multijoueur
    ? [joueurs[playerId]]
    : joueurs
  const ids = new Set<number>()
  for (const joueur of sieges) {
    for (const carte of joueur?.area_hero ?? []) {
      const famille = kindOf(carte)
      if (famille === 'hero' || famille === 'alter-ego') ids.add(carte.id)
    }
  }
  return ids
}

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
 * tomber sous l'une comme sous l'autre. Il se calcule par `herosLocaux`
 * ci-dessus, qui prend TOUS les sièges hors multijoueur.
 *
 * ENSEMBLE VIDE : la défaite compte comme la nôtre, donc l'écran de fin
 * attend. C'est un changement de `5a46f428` (la règle vivait avant ici, et
 * exigeait une cible connue), et il est ASSUMÉ : `area_hero` se vide quand
 * l'identité quitte la table, si bien que l'ensemble peut être vide au moment
 * exact où le coup fatal doit être montré. Rendre faux là ferait paraître
 * l'écran de fin sur la trame même de `game_over`, c'est-à-dire le défaut M5
 * que cette fonction existe pour empêcher. Le risque inverse (retenir l'écran
 * de fin d'un joueur que rien ne concerne) est borné par le filet de temps
 * ci-dessus et par le bouton « Continuer » du cartouche.
 */
export function coupFatalLocal(
  etapes: { defaite?: boolean; cibleId?: number }[],
  herosLocauxIds: Set<number>
): boolean {
  // La MEME regle que la coupe du deroule (`arreterSurDefaite`), et une seule
  // definition : les deux repondent a la question « est-ce NOTRE heros qui
  // vient de tomber ».
  return etapes.some((etape) => estDefaiteLocale(etape, herosLocauxIds))
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
