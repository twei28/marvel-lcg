import { describe, expect, it } from 'vitest'
import { ECHELLE_MIN_PAYSAGE_TEL, SCENE, echelleDeLaTable } from './Board'

describe('echelle de la table', () => {
  it('sur PC, la table tient en entier', () => {
    expect(echelleDeLaTable(1920, 940, 2, false)).toBe(1)
    expect(echelleDeLaTable(1366, 600, 2, false)).toBeCloseTo(Math.min(1366 / SCENE.largeur, 600 / SCENE.hauteur))
  })

  it('telephone couche : jamais sous l echelle minimale lisible', () => {
    const tient = Math.min(844 / SCENE.largeur, 340 / SCENE.hauteur)
    expect(tient).toBeLessThan(ECHELLE_MIN_PAYSAGE_TEL)
    expect(echelleDeLaTable(844, 340, 2, true)).toBe(ECHELLE_MIN_PAYSAGE_TEL)
  })

  it('telephone couche sur un grand ecran : la table qui tient deja ne retrecit pas', () => {
    expect(echelleDeLaTable(1920, 940, 2, true)).toBe(1)
  })
})
