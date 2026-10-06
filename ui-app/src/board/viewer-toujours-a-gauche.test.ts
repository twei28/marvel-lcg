// Le viewer local, toujours a gauche de « Heros et soutiens » (25/09/2026).
//
// Demande de l'utilisateur : « nous toujours a gauche, et les autres a la
// suite ». En vue Auto, `playerId` (transmis a `construirePlateau`) suit
// celui qui doit agir, pas forcement le viewer local : des qu'on suit un
// AUTRE joueur, ses groupes passaient devant ceux du viewer dans
// `terrain-soutien`, et sa zone Heros/soutiens partait visuellement a
// droite. `viewerId` (board.tsx) corrige ca sans toucher a la visibilite
// des cartes, qui reste braquee sur `playerId`.
import { describe, expect, it } from 'vitest'
import { catalogueVide } from './catalogue'
import { construirePlateau } from './zones'
import type { World, WorldPlayer } from './world'

const carte = (id: number, extra: Record<string, unknown> = {}) => ({
  id,
  card_type: 'ally',
  name: `Carte ${id}`,
  card_id: `9900${id}`,
  pic_id: `9900${id}`,
  visible_for_players: [0, 1],
  down_card_ids: [],
  resources: [],
  info: {},
  traits: {},
  buffs: {},
  ...extra,
})

const MOI = 1
const AUTRE = 2

function joueur(heroId: number): unknown {
  return {
    area_hero: [carte(heroId, { card_type: 'hero', name: `Héros ${heroId}` })],
    supports: [],
    allies: [],
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
  }
}

const monde = {
  render_id: 1,
  players: [joueur(MOI) as WorldPlayer, joueur(AUTRE) as WorldPlayer],
  area_villain: [],
  area_schemes_main: [],
} as unknown as World

function proprietairesTerrainSoutien(playerId: number, viewerId?: number): (number | undefined)[] {
  const plateau = construirePlateau(monde, { playerId, viewerId, catalogue: catalogueVide })
  const emplacement = plateau.emplacements.find((e) => e.cle === 'terrain-soutien')
  return emplacement?.proprietaires ?? []
}

describe('le viewer local reste en tete de « Heros et soutiens »', () => {
  it('sans viewerId, comportement inchange : le joueur 0 (playerId) est en tete', () => {
    expect(proprietairesTerrainSoutien(0)[0]).toBe(0)
  })

  it('quand le viewer suit son propre tour (viewerId === playerId), rien ne change', () => {
    expect(proprietairesTerrainSoutien(0, 0)[0]).toBe(0)
  })

  it('quand la vue Auto suit l AUTRE joueur, le viewer local reste quand meme en tete', () => {
    // playerId=1 (on suit le joueur 1, dont c'est le tour) mais viewerId=0
    // (c'est le joueur 0 qui regarde l'ecran).
    expect(proprietairesTerrainSoutien(1, 0)[0]).toBe(0)
  })

  it('et le joueur suivi (playerId) passe bien apres, pas escamote', () => {
    const proprietaires = proprietairesTerrainSoutien(1, 0)
    expect(proprietaires).toContain(1)
    expect(proprietaires.indexOf(0)).toBeLessThan(proprietaires.indexOf(1))
  })
})
