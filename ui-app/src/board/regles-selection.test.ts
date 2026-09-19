// La règle de sélection d'une option, appliquée à la désignation.
//
// Défaut du 18/09/2026 (« Suit Up » 45017) : le plateau lisait `select_rule`
// sans jamais s'en servir, on pouvait composer un choix illégal, et le moteur
// le refusait après coup en défaussant la carte.
import { describe, expect, it } from 'vitest'
import { cibleRefuseeParLaRegle } from './regles-selection'

const carte = (card_id: string, card_type: string) => ({ card_id, card_type })

describe('la règle de sélection', () => {
  it('sans règle, rien n’est jamais refusé', () => {
    expect(cibleRefuseeParLaRegle('', [carte('01074', 'Upgrade')], carte('01065', 'Upgrade'))).toBe(false)
    expect(cibleRefuseeParLaRegle(undefined, [carte('01074', 'Upgrade')], carte('01074', 'Upgrade'))).toBe(false)
  })

  it('DifferentType refuse un second exemplaire du même TYPE', () => {
    const deja = [carte('01074', 'Upgrade')]
    expect(cibleRefuseeParLaRegle('DifferentType', deja, carte('01065', 'Upgrade'))).toBe(true)
    expect(cibleRefuseeParLaRegle('DifferentType', deja, carte('01067', 'Ally'))).toBe(false)
  })

  it('DifferentCards refuse une seconde carte de même TITRE, pas un autre titre du même type', () => {
    const deja = [carte('wx012', 'Upgrade')]
    expect(cibleRefuseeParLaRegle('DifferentCards', deja, carte('wx012', 'Upgrade'))).toBe(true)
    expect(cibleRefuseeParLaRegle('DifferentCards', deja, carte('01074', 'Upgrade'))).toBe(false)
  })

  it('une règle inconnue du plateau ne restreint rien', () => {
    expect(cibleRefuseeParLaRegle('MustIncludeTraits', [carte('01074', 'Upgrade')], carte('01074', 'Upgrade'))).toBe(false)
  })

  it('une cible dont on ignore l’identité ou le type passe', () => {
    expect(cibleRefuseeParLaRegle('DifferentCards', [carte('wx012', 'Upgrade')], { card_type: 'Upgrade' })).toBe(false)
    expect(cibleRefuseeParLaRegle('DifferentType', [carte('wx012', 'Upgrade')], { card_id: 'wx012' })).toBe(false)
  })

  it('la première cible passe toujours', () => {
    expect(cibleRefuseeParLaRegle('DifferentCards', [], carte('wx012', 'Upgrade'))).toBe(false)
    expect(cibleRefuseeParLaRegle('DifferentType', [], carte('wx012', 'Upgrade'))).toBe(false)
  })
})
