// La regle de la tablette (24/10/2026, decision 10) : Auto suit l'appareil, Oui / Non le forcent.
import { afterEach, describe, expect, it } from 'vitest'
import { CLE_JEU_AU_DOIGT, ecrireReglageDoigt, estTablette, lireReglageDoigt, tabletteEffective } from './tablette'

describe('tablette', () => {
  afterEach(() => window.localStorage.removeItem(CLE_JEU_AU_DOIGT))

  it('le reglage l emporte sur l appareil', () => {
    expect(tabletteEffective('auto', true)).toBe(true)
    expect(tabletteEffective('auto', false)).toBe(false)
    expect(tabletteEffective('oui', false)).toBe(true)
    expect(tabletteEffective('non', true)).toBe(false)
  })

  it('retient le reglage et le relit', () => {
    expect(lireReglageDoigt()).toBe('auto')
    ecrireReglageDoigt('oui')
    expect(lireReglageDoigt()).toBe('oui')
    expect(estTablette()).toBe(true)
    ecrireReglageDoigt('non')
    expect(estTablette()).toBe(false)
  })
})
