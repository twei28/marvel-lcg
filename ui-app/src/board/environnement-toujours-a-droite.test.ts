// L'environnement reste toujours du côté droit de « Alliés, sbires et
// environnement » (25/09/2026, demande de l'utilisateur : mieux distinguer
// alliés et sbires dans cette zone qui mélange les deux camps).
//
// Avant, l'environnement se posait juste après NOTRE ligne de combat, donc
// AVANT celle des autres joueurs en multijoueur — il se serait retrouvé au
// milieu de la zone, pas à droite. Ce test verrouille l'ordre : environnement
// toujours en dernier, quel que soit le nombre de joueurs.
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
const MON_ENGAGE = 11
const ALLIE_AUTRE = 20
const ENGAGE_AUTRE = 21
const ENVIRONNEMENT = 90

function joueur(heroId: number, allieId: number, engageId: number): unknown {
  return {
    area_hero: [carte(heroId, { card_type: 'hero', name: `Héros ${heroId}` })],
    supports: [],
    allies: [carte(allieId)],
    obligations_area: [],
    engaged_enemies: [carte(engageId, { card_type: 'minion' })],
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

function plateauAvec(nombreDeJoueurs: 1 | 2) {
  const joueurs = [joueur(MOI, MON_ALLIE, MON_ENGAGE) as WorldPlayer]
  if (nombreDeJoueurs === 2) joueurs.push(joueur(AUTRE, ALLIE_AUTRE, ENGAGE_AUTRE) as WorldPlayer)
  const monde = {
    render_id: 1,
    players: joueurs,
    area_villain: [],
    area_schemes_main: [],
    area_environment: [carte(ENVIRONNEMENT, { card_type: 'MainScheme' })],
  } as unknown as World
  return construirePlateau(monde, { playerId: 0, catalogue: catalogueVide })
}

function idsDesGroupes(nombreDeJoueurs: 1 | 2): string[][] {
  const plateau = plateauAvec(nombreDeJoueurs)
  const emplacement = plateau.emplacements.find((e) => e.cle === 'terrain-combat')
  return (emplacement?.groupes ?? []).map((groupe) => groupe.map((u: any) => u.carte?.id))
}

describe('« Alliés, sbires et environnement » : l’environnement reste a droite', () => {
  it('en solo, l’environnement est le dernier groupe', () => {
    const groupes = idsDesGroupes(1)
    expect(groupes[groupes.length - 1]).toContain(String(ENVIRONNEMENT))
  })

  it('en multijoueur, l’environnement reste APRES la ligne de combat de TOUS les joueurs', () => {
    const groupes = idsDesGroupes(2)
    const indexEnvironnement = groupes.findIndex((g) => g.includes(String(ENVIRONNEMENT)))
    const indexAutre = groupes.findIndex(
      (g) => g.includes(String(ALLIE_AUTRE)) || g.includes(String(ENGAGE_AUTRE))
    )
    expect(indexEnvironnement).toBeGreaterThan(-1)
    expect(indexAutre).toBeGreaterThan(-1)
    expect(indexEnvironnement).toBeGreaterThan(indexAutre)
  })
})
