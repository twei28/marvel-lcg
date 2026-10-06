// proprietaire.ts — à qui est une carte, et qui peut la bouger (lot 5 du
// 06/10/2026, question 14 : « comme OCTGN, chacun ne bouge que ses propres
// cartes ; les cartes Rencontre sont à tous »).
//
// Le propriétaire se lit dans les zones de CARTES DE JOUEUR d'un siège. Une
// carte Rencontre posée chez un joueur (sbire engagé, obligation, traîtrise
// distribuée) reste à tous. Fonctions PURES.
import type { World, WorldCard, WorldPlayer } from '../world'

const zonesDuJoueur = (joueur: WorldPlayer): (WorldCard[] | undefined)[] => [
  joueur.hand_cards,
  joueur.player_deck,
  joueur.player_discard_pile,
  joueur.area_hero,
  joueur.allies,
  joueur.supports,
  joueur.reserve,
  joueur.rising_tide,
  joueur.area_processing,
  joueur.additional_deck,
  joueur.additional_discard_pile,
]

/** Le siège (rang dans `world.players`) dont la carte est une carte de joueur, ou `undefined` (Rencontre, inconnue). */
export function proprietaireDe(world: World | undefined, id: number): number | undefined {
  const joueurs = world?.players ?? []
  for (let siege = 0; siege < joueurs.length; siege++) {
    if (zonesDuJoueur(joueurs[siege]).some((zone) => (zone ?? []).some((carte) => Number(carte.id) === id))) {
      return siege
    }
  }
  return undefined
}

/** Les sièges que cet écran joue : tous à une même table, le sien seul en ligne. */
export function siegesControles(world: World | undefined, monSiege: number, multijoueur: boolean): number[] {
  if (multijoueur) return [monSiege]
  return (world?.players ?? []).map((_, siege) => siege)
}

/** Une carte de joueur ne bouge que par l'écran qui tient son siège ; une carte Rencontre, par tous. */
export function peutBouger(world: World | undefined, id: number, controles: number[]): boolean {
  const proprietaire = proprietaireDe(world, id)
  return proprietaire === undefined || controles.includes(proprietaire)
}
