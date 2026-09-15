import { describe, expect, it } from 'vitest'
import { AJUSTEMENT_MINIMUM, ajustementDuCartouche, placeDisponible } from './ajustement-cartouche'

describe('ajustementDuCartouche', () => {
  it('ne change rien quand tout tient', () => {
    expect(ajustementDuCartouche(400, 600)).toBe(1)
  })

  it('⚠ n AGRANDIT jamais un cartouche qui a de la place', () => {
    // Le temoin : sans lui, `disponible / naturel` gonflerait le cartouche sur
    // les grands ecrans, ce que personne n'a demande.
    expect(ajustementDuCartouche(200, 900)).toBe(1)
  })

  it('retrecit juste ce qu il faut', () => {
    // Le cas mesure chez l'utilisateur : 809 px de contenu, 595 px de place.
    expect(ajustementDuCartouche(809, 595)).toBeCloseTo(595 / 809, 3)
  })

  it('ne descend pas sous le plancher de lisibilite', () => {
    expect(ajustementDuCartouche(4000, 400)).toBe(AJUSTEMENT_MINIMUM)
  })

  it('se tait devant une mesure absente ou absurde', () => {
    expect(ajustementDuCartouche(0, 600)).toBe(1)
    expect(ajustementDuCartouche(800, 0)).toBe(1)
    expect(ajustementDuCartouche(Number.NaN, 600)).toBe(1)
  })
})

describe('placeDisponible', () => {
  it('retranche le bord bas et la marge du haut', () => {
    expect(placeDisponible(663, 52)).toBe(595)
  })

  it('ne rend jamais de place negative', () => {
    expect(placeDisponible(200, 400)).toBe(0)
  })
})
