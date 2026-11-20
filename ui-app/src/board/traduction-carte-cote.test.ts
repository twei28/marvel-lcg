import { describe, expect, it } from 'vitest'
import { coteDuTexte } from './traduction-carte'

describe('coteDuTexte : de quel côté la manigance écrit son texte', () => {
  it('manigance principale à gauche ; annexe des méchants ET de joueur à droite', () => {
    expect(coteDuTexte('MainScheme')).toBe('gauche')
    expect(coteDuTexte('SideScheme')).toBe('droite')
    expect(coteDuTexte('PlayerSideScheme')).toBe('droite')
  })

  it('aucun côté pour une carte qui n\'est pas une manigance', () => {
    expect(coteDuTexte('Minion')).toBeUndefined()
    expect(coteDuTexte(undefined)).toBeUndefined()
  })
})
