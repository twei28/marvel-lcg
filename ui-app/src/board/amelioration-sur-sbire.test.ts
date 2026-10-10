// Une amelioration du JOUEUR posee sur un SBIRE engage doit se voir.
//
// Audit Luke Cage du 10/10/2026 : `62009` Cruisin' for a Bruisin' se posait sur
// l'identite au lieu du sbire. Corrige cote moteur, la carte arrive maintenant
// sous un ennemi engage, comme `ar008` Reeling. Ce cas verrouille que le plateau
// la dessine bien la, et qu'elle ne fuit pas sur l'identite.
import { describe, expect, it } from 'vitest'
import { carteSurTable, dessinee, siege, tableAvec } from './plateau-de-test'

const IDENTITE = 1
const SBIRE = 81
const CRUISIN = 19

const monde = () =>
  tableAvec(
    siege({
      area_hero: [carteSurTable(IDENTITE, '62001a', 'Hero', 'Luke Cage')],
      engaged_enemies: [
        carteSurTable(SBIRE, '01182', 'Minion', 'Hydra Soldier'),
        carteSurTable(CRUISIN, '62009', 'Upgrade', "Cruisin' for a Bruisin'", {
          bind_object_id: SBIRE,
        }),
      ],
    })
  )

describe('amelioration du joueur sur un sbire engage', () => {
  it('dessine Cruisin for a Bruisin sous le sbire', () => {
    expect(dessinee(monde(), CRUISIN)).toBeDefined()
    expect(dessinee(monde(), SBIRE)).toBeDefined()
  })

  it('temoin : une carte absente de la table n est pas dessinee', () => {
    expect(dessinee(monde(), 999)).toBeUndefined()
  })
})
