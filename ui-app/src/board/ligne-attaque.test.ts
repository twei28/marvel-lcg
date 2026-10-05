import { describe, expect, it } from 'vitest'
import type { Option } from './ask'
import { detailAttaqueComplet, ligneAttaqueConnue, ligneDefense } from './ligne-attaque'
import type { WorldCard } from './world'

const carte = (id: number, surcharge: Partial<WorldCard> = {}): WorldCard =>
  ({ id, bind_object_id: 0, is_face_up: true, info: {}, ...surcharge }) as unknown as WorldCard
const defense = (attaquant: number) =>
  [{ name: 'Defense', all_legal_targets: [attaquant] }] as unknown as Option[]

describe('sous « Ne pas défendre », seulement ce qui est connu', () => {
  it('ATQ actuelle et cartes boost face cachee, sans total', () => {
    const cartes = new Map([
      [10, carte(10, { info: { attack: 3 } })],
      [11, carte(11, { bind_object_id: 10, is_face_up: false })],
    ])
    expect(ligneAttaqueConnue(defense(10), cartes)).toBe('ATQ 3 + 1 carte boost')
  })

  it('deux boosts (phase 3 du mechant, effets…) : au pluriel', () => {
    const cartes = new Map([
      [10, carte(10, { info: { attack: 4 } })],
      [11, carte(11, { bind_object_id: 10, is_face_up: false })],
      [12, carte(12, { bind_object_id: 10, is_face_up: false })],
    ])
    expect(ligneAttaqueConnue(defense(10), cartes)).toBe('ATQ 4 + 2 cartes boost')
  })

  it('sbire sans boost : l ATQ seule ; une amelioration visible attachee ne compte pas', () => {
    const cartes = new Map([
      [20, carte(20, { info: { attack: 2 } })],
      [21, carte(21, { bind_object_id: 20, is_face_up: true })],
    ])
    expect(ligneAttaqueConnue(defense(20), cartes)).toBe('ATQ 2')
  })

  it('un deck rattache au vilain (Armes Experimentales) ne compte pas comme des boosts', () => {
    const cartes = new Map([
      [10, carte(10, { info: { attack: 1 } })],
      [11, carte(11, { bind_object_id: 10, is_face_up: false })],
      [12, carte(12, { bind_object_id: 10, is_face_up: false })],
      [13, carte(13, { bind_object_id: 10, is_face_up: false })],
      [14, carte(14, { bind_object_id: 10, is_face_up: false })],
    ])
    const deck = new Set([12, 13, 14])
    expect(ligneAttaqueConnue(defense(10), cartes, undefined, deck)).toBe('ATQ 1 + 1 carte boost')
    expect(detailAttaqueComplet(defense(10), cartes, undefined, deck)).toBe('ATQ 1 + 1 carte boost')
  })

  it('pas de question de defense : rien', () => {
    expect(ligneAttaqueConnue([], new Map())).toBeUndefined()
  })
})

// Decision du 04/10/2026 (questions une a une) : chaque bonus nomme avec sa
// carte (publie par le moteur, `bonus`), deux au plus ; au-dela, les points
// restants en « + N autres », detail complet au survol ; les boosts toujours.
describe('le detail des bonus, carte par carte', () => {
  const bonus = (...b: [string, number, number][]) => ({ ATK: b })

  it('nomme le bonus et sa carte, puis les boosts', () => {
    const cartes = new Map([
      [10, carte(10, { info: { attack: 5 }, bonus: bonus(['Charge', 52, 3]) })],
      [11, carte(11, { bind_object_id: 10, is_face_up: false })],
    ])
    expect(ligneAttaqueConnue(defense(10), cartes)).toBe('ATQ 2 + 3 Charge + 1 carte boost')
  })

  it('au-dela de deux bonus : les points restants en « autres », tout au survol', () => {
    const cartes = new Map([
      [10, carte(10, {
        info: { attack: 7 },
        bonus: bonus(['Armure', 1, 1], ['Charge', 2, 1], ['Rage', 3, 1], ['Furie', 4, 2]),
      })],
      [11, carte(11, { bind_object_id: 10, is_face_up: false })],
    ])
    expect(ligneAttaqueConnue(defense(10), cartes)).toBe('ATQ 2 + 1 Armure + 1 Charge + 3 autres + 1 carte boost')
    expect(detailAttaqueComplet(defense(10), cartes)).toBe(
      'ATQ 2 + 1 Armure + 1 Charge + 1 Rage + 2 Furie + 1 carte boost'
    )
  })

  it('un malus se dit avec un moins, et le nom de la carte en francais quand on le connait', () => {
    const cartes = new Map([[10, carte(10, { info: { attack: 2 }, bonus: bonus(['Weakened', 60, -1]) })]])
    expect(ligneAttaqueConnue(defense(10), cartes, (id) => (id === 60 ? 'Affaibli' : undefined))).toBe('ATQ 3 − 1 Affaibli')
  })

  it('la DEF du defenseur, meme regle', () => {
    const jessica = carte(30, { info: { defense: 3 }, bonus: { DEF: [['Bouclier', 31, 1]] } })
    expect(ligneDefense(jessica)).toBe('DÉF 2 + 1 Bouclier')
    expect(ligneDefense(carte(32, { info: { defense: 1 } }))).toBe('DÉF 1')
    expect(ligneDefense(carte(33, { info: {} }))).toBeUndefined()
  })
})
