// Regarder UN joueur, c'est ne voir que sa partie.
//
// Le selecteur « Vue » de la barre du haut a deux regimes, et ils n'avaient pas
// de difference visible sur la table :
//
//   - « Auto » suit celui qui doit agir. La table montre tout le monde, ce qui
//     est le propre d'une partie a plusieurs : les allies et les ennemis engages
//     des autres joueurs partagent la ligne de combat, chacun avec le nom de son
//     proprietaire en badge.
//   - Cliquer sur UN joueur, en revanche, doit poser la table de CE joueur.
//     C'etait seulement sa main et ses actions qui changeaient ; ses voisins
//     restaient etales sur le terrain, et on cherchait ses propres cartes au
//     milieu de celles des autres.
//
// Ce qui appartient a la table COMMUNE (mechant, complot principal, complots
// annexes, environnement, deck rencontre) reste visible dans les deux cas : ce
// n'est a personne, et une partie sans mechant ne veut rien dire.
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
const MON_ALLIE = 10
const MON_SOUTIEN = 11
const ALLIE_AUTRE = 20
const SOUTIEN_AUTRE = 21
const ENNEMI_AUTRE = 22
const MECHANT = 90
const COMPLOT = 91

function joueur(heroId: number, allieId: number, soutienId: number, ennemiId?: number): unknown {
  return {
    area_hero: [carte(heroId, { card_type: 'hero', name: `Héros ${heroId}` })],
    supports: [carte(soutienId, { card_type: 'support' })],
    allies: [carte(allieId)],
    obligations_area: [],
    engaged_enemies: ennemiId ? [carte(ennemiId, { card_type: 'minion' })] : [],
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
  players: [
    joueur(MOI, MON_ALLIE, MON_SOUTIEN) as WorldPlayer,
    joueur(AUTRE, ALLIE_AUTRE, SOUTIEN_AUTRE, ENNEMI_AUTRE) as WorldPlayer,
  ],
  area_villain: [carte(MECHANT, { card_type: 'EncounterVillain' })],
  area_schemes_main: [carte(COMPLOT, { card_type: 'MainScheme' })],
} as unknown as World

const surLaTable = (seulCeJoueur: boolean): Set<number> =>
  construirePlateau(monde, { playerId: 0, catalogue: catalogueVide, seulCeJoueur }).idsAffiches

describe('vue braquee sur un seul joueur', () => {
  it('montre tout le monde tant qu on ne choisit personne', () => {
    const ids = surLaTable(false)
    expect(ids).toContain(MOI)
    expect(ids).toContain(AUTRE)
    expect(ids).toContain(ALLIE_AUTRE)
    expect(ids).toContain(SOUTIEN_AUTRE)
  })

  it('ecarte le heros des autres joueurs', () => {
    expect(surLaTable(true)).not.toContain(AUTRE)
  })

  it('ecarte leurs allies et leurs soutiens', () => {
    const ids = surLaTable(true)
    expect(ids).not.toContain(ALLIE_AUTRE)
    expect(ids).not.toContain(SOUTIEN_AUTRE)
  })

  it('ecarte les ennemis engages avec eux', () => {
    expect(surLaTable(true)).not.toContain(ENNEMI_AUTRE)
  })

  it('garde INTACTE l aire du joueur regarde', () => {
    const ids = surLaTable(true)
    expect(ids).toContain(MOI)
    expect(ids).toContain(MON_ALLIE)
    expect(ids).toContain(MON_SOUTIEN)
  })

  it('garde la table commune : le mechant et le complot ne sont a personne', () => {
    const ids = surLaTable(true)
    expect(ids).toContain(MECHANT)
    expect(ids).toContain(COMPLOT)
  })
})
