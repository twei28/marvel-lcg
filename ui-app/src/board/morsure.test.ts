// Marqueur de MORSURE (Alligator Loki, Lock Jaws) : le moteur pose
// `held_by_hero` (numero du joueur, 0 = personne) sur l'ennemi tenu et
// `attached_to_enemy` sur le heros accroche. Le modele les traduit en deux
// drapeaux d'affichage, `mordu` et `accroche`, et rien d'autre ne change.
import { describe, expect, it } from 'vitest'
import { toScanCard, type ContexteCarte } from './card-model'
import { catalogueVide } from './catalogue'
import type { WorldCard } from './world'

function carte(card_type: string, info: Record<string, number>): WorldCard {
  return {
    id: 9,
    bind_object_id: 0,
    name: 'Shocker',
    info,
    traits: {},
    buffs: {},
    card_id: '01103',
    pic_id: '01103',
    down_card_ids: [],
    card_type,
    is_face_up: true,
    is_ready: true,
    visible_for_players: [0],
  } as unknown as WorldCard
}

const contexte: ContexteCarte = {
  playerId: 0,
  actives: new Set<number>(),
  catalogue: catalogueVide,
}

describe('marqueur de morsure', () => {
  it('marque l’ennemi tenu par un heros', () => {
    const props = toScanCard(carte('Minion', { health: 3, held_by_hero: 1 }), contexte)
    expect(props.mordu).toBe(true)
    expect(props.accroche).toBe(false)
  })

  it('ne marque pas un ennemi libre (0 = personne)', () => {
    const props = toScanCard(carte('Minion', { health: 3, held_by_hero: 0 }), contexte)
    expect(props.mordu).toBe(false)
  })

  it('reste muet quand le moteur ne dit rien', () => {
    const props = toScanCard(carte('Minion', { health: 3 }), contexte)
    expect(props.mordu).toBe(false)
    expect(props.accroche).toBe(false)
  })

  it('marque le heros accroche', () => {
    const props = toScanCard(carte('Hero', { health: 9, attached_to_enemy: 1 }), contexte)
    expect(props.accroche).toBe(true)
    expect(props.mordu).toBe(false)
  })
})
