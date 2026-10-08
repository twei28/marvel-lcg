import { describe, expect, it } from 'vitest'
import { paiementNulDUneAutreCarte, type Option } from './ask'

function option(surcharge: Partial<Option>): Option {
  return {
    id: 1,
    name: 'Spend_of_any_type',
    bind_id: 82,
    bind_player_id: 0,
    all_legal_targets: [],
    target_num_range: [0, 0],
    target_payment: { 0: { cost: '0', payment: [{ effect_id: 40, res_text: 'RR' }], rule: [], warning: {} } },
    select_rule: '',
    target_must_include_traits: [],
    failure_reason: '',
    is_search: false,
    ...surcharge,
  } as Option
}

describe('fenetre de paiement nul ouverte pour une autre carte (rapport Phocea n65)', () => {
  it('Make the Call paie le cout 0 d Ant-Man : on peut surpayer, pas de validation courte', () => {
    expect(paiementNulDUneAutreCarte(option({}))).toBe(true)
  })
  it('un vrai cout n est pas concerne', () => {
    const o = option({
      target_payment: { 0: { cost: '2', payment: [{ effect_id: 40, res_text: 'RR' }], rule: [], warning: {} } },
    } as Partial<Option>)
    expect(paiementNulDUneAutreCarte(o)).toBe(false)
  })
  it('une option avec cibles (jouer une carte) n est pas concernee', () => {
    expect(paiementNulDUneAutreCarte(option({ name: 'Play', all_legal_targets: [81] }))).toBe(false)
  })
  it('rien a depenser : pas de fenetre', () => {
    const o = option({
      target_payment: { 0: { cost: '0', payment: [], rule: [], warning: {} } },
    } as Partial<Option>)
    expect(paiementNulDUneAutreCarte(o)).toBe(false)
  })
})
