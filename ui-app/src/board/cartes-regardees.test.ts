// Rapport Yarro n85 (15/10/2026) : avec Rocket Raccoon, chaque Salvage remet
// une amelioration Tech de la defausse sur le deck, et la fenetre « Cartes
// regardees » se rouvrait a chaque fois. Une carte passee par la defausse est
// CONNUE de tous (`visible_for_players`) sans avoir ete REGARDEE (`looked_at_by`).
import { describe, expect, it } from 'vitest'
import { estRegardeePar, type WorldCard } from './world'

const carte = (extra: Partial<WorldCard>): WorldCard => ({
  id: 21,
  is_ready: true,
  is_face_up: false,
  visible_for_players: [0],
  bind_object_id: 0,
  name: "Rocket's Pistol",
  info: {},
  traits: {},
  buffs: {},
  card_id: '16038',
  pic_id: '16038',
  down_card_ids: [],
  card_type: 'Upgrade',
  cost: 1,
  resources: [],
  ...extra,
})

describe('estRegardeePar', () => {
  it('une carte remise de la defausse sur le deck est connue, pas regardee', () => {
    expect(estRegardeePar(carte({ looked_at_by: [] }), 0)).toBe(false)
  })

  it('une carte regardee par un effet l est', () => {
    expect(estRegardeePar(carte({ looked_at_by: [0] }), 0)).toBe(true)
    expect(estRegardeePar(carte({ looked_at_by: [1] }), 0)).toBe(false)
  })

  it('moteur sans `looked_at_by` : l ancienne regle (visible = regardee)', () => {
    expect(estRegardeePar(carte({}), 0)).toBe(true)
    expect(estRegardeePar(carte({ visible_for_players: [] }), 0)).toBe(false)
  })
})
