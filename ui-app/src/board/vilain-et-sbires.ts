// « Le vilain et chaque sbire engage avec UN joueur » (VillainAndMinionsEngagedSamePlayer : Morsure d'araignees de Shuri, Rocket Raccoon...).
//
// Le moteur annonce TOUS les candidats (le vilain et les sbires de TOUS les joueurs) avec un nombre de cibles egal a leur total, mais sa
// verification (`SelectorRule.AfterSelectTargets`) ne demande que ceci : les sbires choisis sont engages avec le MEME joueur. A plusieurs
// joueurs engages, exiger le total est donc impossible a satisfaire : il faut choisir un joueur, puis viser le vilain et SES sbires.

import type { Option } from './ask'
import type { World } from './world'

export type GroupesVilainSbires = {
  vilains: number[]
  /** Les sbires candidats, par place du joueur auquel ils sont engages. */
  parJoueur: Map<number, number[]>
}

export const REGLE_MEME_JOUEUR = 'VillainAndMinionsEngagedSamePlayer'

export function groupesVilainEtSbires(option: Option, world: World | undefined): GroupesVilainSbires | undefined {
  if (option.select_rule !== REGLE_MEME_JOUEUR || !world?.players) return undefined
  const candidats = new Set(option.all_legal_targets)
  const parJoueur = new Map<number, number[]>()
  const sbires = new Set<number>()
  world.players.forEach((joueur, place) => {
    const siens = (joueur.engaged_enemies ?? []).map((carte) => carte.id).filter((id) => candidats.has(id))
    if (siens.length === 0) return
    parJoueur.set(place, siens)
    siens.forEach((id) => sbires.add(id))
  })
  const vilains = [...candidats].filter((id) => !sbires.has(id))
  return { vilains, parJoueur }
}

/** Plusieurs joueurs ont des sbires candidats : c'est le seul cas ou le moteur laisse un vrai choix. */
export function choixDeJoueurNecessaire(groupes: GroupesVilainSbires | undefined): groupes is GroupesVilainSbires {
  return groupes !== undefined && groupes.parJoueur.size > 1
}

/** Le joueur retenu : celui du premier sbire deja coche, sinon le joueur qui agit, sinon le premier engage. */
export function joueurRetenu(groupes: GroupesVilainSbires, cibles: readonly number[], placeActeur: number): number {
  for (const id of cibles) {
    for (const [place, sbires] of groupes.parJoueur) if (sbires.includes(id)) return place
  }
  return groupes.parJoueur.has(placeActeur) ? placeActeur : [...groupes.parJoueur.keys()][0]!
}

export function selectionDuJoueur(groupes: GroupesVilainSbires, place: number): number[] {
  return [...groupes.vilains, ...(groupes.parJoueur.get(place) ?? [])]
}

/** L'option telle que le joueur la vit : le vilain et les sbires du joueur retenu sont exiges, rien d'autre. */
export function optionPourJoueur(option: Option, groupes: GroupesVilainSbires, place: number): Option {
  const exige = selectionDuJoueur(groupes, place).length
  return { ...option, target_num_range: [exige, option.all_legal_targets.length] }
}
