// Les cartes mises de côté tiennent en DEUX piles seulement (demande du
// 05/10/2026) : une ouverte (set némésis, victoire, retirées...) qui se lit
// groupée par origine, une masquée dont le clic dit d'où viennent les cartes
// et combien il y en a, sans jamais les montrer.
import { describe, expect, it } from 'vitest'
import { catalogueVide } from './catalogue'
import { construirePlateau, type UniteAffichee } from './zones'
import type { World } from './world'

const carte = (id: number, type: string, nom: string) => ({
  id,
  card_type: type,
  name: nom,
  card_id: `9900${id}`,
  pic_id: `9900${id}`,
  visible_for_players: [0],
  down_card_ids: [],
  resources: [],
  info: {},
  traits: {},
  buffs: {},
})

function monde(joueur: Record<string, unknown>, victoire: unknown[] = []): World {
  return {
    render_id: 1,
    victory_display: victoire,
    players: [
      {
        area_hero: [],
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
        ...joueur,
      },
    ],
  } as unknown as World
}

function annexes(world: World): UniteAffichee[] {
  const plateau = construirePlateau(world, { playerId: 0, catalogue: catalogueVide })
  return plateau.emplacements.filter((e) => e.cle === 'annexes').flatMap((e) => e.groupes.flat())
}

describe('piles des mises de côté', () => {
  it('range le set némésis dans la pile ouverte, sous son propre titre', () => {
    const unites = annexes(
      monde({ set_aside_nemesis_sets: [carte(1, 'Minion', 'Vulture')] }, [carte(2, 'Villain', 'Rhino')])
    )
    expect(unites.map((u) => u.cle)).toEqual(['annexes-visibles'])
    const groupes = unites[0].pileGroupes ?? []
    expect(groupes.map((g) => [g.cle, g.cartes.length])).toEqual([
      ['nemesis', 1],
      ['victoire', 1],
    ])
    expect(groupes.every((g) => g.masque === undefined)).toBe(true)
  })

  it('la pile masquée donne les noms et les nombres, jamais les cartes', () => {
    const unites = annexes(monde({ set_aside_deck: [carte(3, 'Event', 'A'), carte(4, 'Event', 'B')] }))
    expect(unites.map((u) => u.cle)).toEqual(['annexes-cachees'])
    const [pile] = unites
    expect(pile.pileGroupes).toEqual([
      { cle: 'mise-de-cote', titre: expect.any(String), cartes: [], masque: { nombre: 2 } },
    ])
    expect(pile.pileContenu).toEqual([])
  })

  it('ne dessine pas une pile vide', () => {
    expect(annexes(monde({}))).toEqual([])
  })
})
