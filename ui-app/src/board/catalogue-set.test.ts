import { describe, expect, it } from 'vitest'
import { catalogueVide, construire } from './catalogue'

describe('le set de chaque carte (Choisir un set, mode manuel)', () => {
  it('vient de set_name dans cards.json', () => {
    const c = construire({ gob: [{ card_id: '01103', name: 'Hydra Mercs', set_name: 'Risky Business' }, { card_id: 'x' }] })
    expect(c.set('01103')).toBe('Risky Business')
    expect(c.set('x')).toBeUndefined()
    expect(catalogueVide.set('01103')).toBeUndefined()
  })
})
