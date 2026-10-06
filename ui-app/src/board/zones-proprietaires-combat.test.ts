// Lot 5 du 06/10/2026 (question 6) : la ligne de combat aplatit les alliés et
// ennemis engagés de TOUS les joueurs. Chaque groupe garde son siège, pour
// qu'une carte lâchée dans le groupe d'un joueur arrive chez lui.
import { describe, expect, it } from 'vitest'
import { catalogueVide } from './catalogue'
import { construirePlateau } from './zones'
import type { World, WorldPlayer } from './world'

const carte = (id: number, type: string) => ({
  id,
  card_type: type,
  name: `Carte ${id}`,
  card_id: `9900${id}`,
  pic_id: `9900${id}`,
  visible_for_players: [0, 1],
  down_card_ids: [],
  resources: [],
  info: {},
  traits: {},
  buffs: {},
})

function joueur(heroId: number, allieId: number): WorldPlayer {
  return {
    area_hero: [carte(heroId, 'Hero')],
    supports: [],
    allies: [carte(allieId, 'Ally')],
    obligations_area: [],
    engaged_enemies: [],
    environment_area: [],
    hand_cards: [],
    reserve: [],
    player_deck: [],
    player_discard_pile: [],
    additional_deck: [],
    additional_discard_pile: [],
    set_aside_deck: [],
    set_aside_nemesis_sets: [],
    resources: '',
    is_eliminated: false,
  } as unknown as WorldPlayer
}

const monde = {
  render_id: 1,
  players: [joueur(1, 11), joueur(2, 22)],
  area_villain: [],
  area_schemes_main: [],
  area_environment: [carte(33, 'Environment')],
} as unknown as World

describe('la ligne de combat garde le siège de chaque groupe', () => {
  it('allié du siège 0, allié du siège 1, environnement à personne', () => {
    const plateau = construirePlateau(monde, { playerId: 0, catalogue: catalogueVide })
    const combat = plateau.emplacements.find((e) => e.cle === 'terrain-combat')
    expect(combat?.proprietaires).toEqual([0, 1, undefined])
  })
})
