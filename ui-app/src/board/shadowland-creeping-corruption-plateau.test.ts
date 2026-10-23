// Shadowland, Heart of Shadow : Creeping Corruption (sl072a/b) est attachee a l'identite ; ses compteurs decident de la partie, la carte
// se pose donc A COTE de l'identite, en entier, au lieu de se glisser dessous (23/10/2026).
import { describe, expect, it } from 'vitest'
import { carteSurTable as carte, dessinee, siege, tableAvec } from './plateau-de-test'

const monde = () =>
  tableAvec(
    siege({
      area_hero: [
        carte(1, 'sl072a', 'Upgrade', 'Creeping Corruption', { bind_object_id: 1000 }),
        carte(1000, '01001b', 'AlterEgo', 'Peter Parker'),
        carte(11, '01088', 'Upgrade', 'Autre amelioration', { bind_object_id: 1000 }),
      ],
    })
  )

describe('Creeping Corruption sur la table', () => {
  it("n'est plus portee par l'identite : elle est posee a cote, en entier", () => {
    // `portePar: 0` = carte posee seule (convention de plateau-de-test) ; sinon l'identifiant du porteur
    expect(dessinee(monde(), 1)?.portePar).toBe(0)
    expect(dessinee(monde(), 1)?.zone).toBe('terrain-soutien')
  })
  it('une amelioration ordinaire reste glissee sous son porteur', () => {
    expect(dessinee(monde(), 11)?.portePar).toBe(1000)
  })
})
