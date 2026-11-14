// La Damnation du scénario Mephisto : UNE pile par joueur, face cachée pour
// tous, dans les annexes (zone commune) pour que chaque camp voie le compteur
// des autres. Le clic dit combien de cartes, jamais lesquelles.
import { describe, expect, it } from 'vitest'
import { catalogueVide } from './catalogue'
import { construirePlateau, type UniteAffichee } from './zones'
import type { World } from './world'

const carte = (id: number, nom: string) => ({
  id,
  card_type: 'Event',
  name: nom,
  card_id: `9900${id}`,
  pic_id: `9900${id}`,
  visible_for_players: [],
  down_card_ids: ['player'],
  resources: [],
  info: {},
  traits: {},
  buffs: {},
})

const joueur = (nom: string, damnation?: unknown[]) => ({
  area_hero: [{ ...carte(900, nom), card_type: 'Hero' }],
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
  ...(damnation ? { damnation } : {}),
})

const monde = (...joueurs: unknown[]): World =>
  ({ render_id: 1, players: joueurs } as unknown as World)

function annexes(world: World, playerId = 0): UniteAffichee[] {
  const plateau = construirePlateau(world, { playerId, catalogue: catalogueVide })
  return plateau.emplacements.filter((e) => e.cle === 'annexes').flatMap((e) => e.groupes.flat())
}

describe('Damnation (pack Mephisto)', () => {
  it('une pile cachée par joueur, avec son compteur, visible de chaque camp', () => {
    const world = monde(
      joueur('Spider-Man', [carte(1, 'A'), carte(2, 'B'), carte(3, 'C')]),
      joueur('Hawkeye', [carte(4, 'D')])
    )
    for (const siege of [0, 1]) {
      const unites = annexes(world, siege)
      expect(unites.map((u) => u.cle)).toEqual(['damnation-0-cachees', 'damnation-1-cachees'])
      expect(unites.map((u) => u.carte.pileCount)).toEqual([3, 1])
      expect(unites.map((u) => u.carte.facedown)).toEqual([true, true])
    }
  })

  it('ne montre jamais les cartes : seul le nombre', () => {
    const [pile] = annexes(monde(joueur('Spider-Man', [carte(1, 'A'), carte(2, 'B')])))
    expect(pile.pileContenu).toEqual([])
    expect(pile.pileGroupes?.map((g) => [g.cartes.length, g.masque])).toEqual([[0, { nombre: 2 }]])
    expect(pile.carte.imageUrl).not.toContain('9900')
  })

  it('porte une étiquette lisible sur la table : « Damnation », et le héros à plusieurs joueurs', () => {
    const [seule] = annexes(monde(joueur('Spider-Man', [carte(1, 'A')])))
    expect(seule.etiquette).toBe('Damnation')
    const deux = annexes(monde(joueur('Spider-Man', [carte(1, 'A')]), joueur('Hawkeye', [carte(4, 'D')])))
    expect(deux.map((u) => u.etiquette)).toEqual(['Damnation\nSpider-Man', 'Damnation\nHawkeye'])
  })

  it('ne dessine rien quand la Damnation est vide ou absente (hors Mephisto)', () => {
    expect(annexes(monde(joueur('Spider-Man', [])))).toEqual([])
    expect(annexes(monde(joueur('Spider-Man')))).toEqual([])
  })

  it('un joueur éliminé n’a plus de pile', () => {
    const elimine = { ...joueur('Hawkeye', [carte(4, 'D')]), is_eliminated: true }
    const unites = annexes(monde(joueur('Spider-Man', [carte(1, 'A')]), elimine))
    expect(unites.map((u) => u.cle)).toEqual(['damnation-0-cachees'])
  })
})
