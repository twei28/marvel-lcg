import { describe, expect, it } from 'vitest'
import { ligneDeStat } from './FeuilleDetail'

describe('ligneDeStat (decision Q71)', () => {
  it('dit la valeur imprimee et l ecart quand elle est modifiee', () => {
    expect(ligneDeStat({ label: 'ATK', value: 3, base: 2 })).toEqual({ nom: 'ATQ', texte: '3 (2 +1)', sens: 'plus' })
    expect(ligneDeStat({ label: 'SCH', value: 1, base: 2 })).toEqual({ nom: 'MNG', texte: '1 (2 −1)', sens: 'moins' })
  })
  it('reste simple quand rien ne change', () => {
    expect(ligneDeStat({ label: 'DEF', value: 2, base: 2 })).toEqual({ nom: 'DÉF', texte: '2', sens: 'egal' })
    expect(ligneDeStat({ label: 'REC', value: 3 })).toEqual({ nom: 'REC', texte: '3', sens: 'egal' })
  })
})
