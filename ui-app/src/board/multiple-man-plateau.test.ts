// Multiple Man / Jamie Madrox (mm001a/b) : ce que la table DESSINE (étape 8 bis de PROCESSUS-CARTE).
//  - mm002/mm003 : deux alliés Dupe (même nom, cartes distinctes) ; mm015 Kinetic Absorption Suit : amélioration SANS « Attach to » (extension de l'identité) ;
//    mm016 X-Factor Investigations : soutien ;
//  - mm012 Madrox Prime et mm014 Prepare For Future Tragedy : complots annexes JOUEUR (paysage) ; mm018 Who's Killing Dupes? : complot annexe de rencontre (paysage) ;
//  - mm019 Emperor Madrox : sbire némésis engagé ; mm020 Dupes Gone Bad : sbire engagé.
// Le dessin de ces types est générique (`zones.ts`) : ce cas le vaut pour Multiple Man.
import { describe, expect, it } from 'vitest'
import { carteSurTable, dessinee, siege, tableAvec } from './plateau-de-test'

const MM = 1
const DUPE1 = 2
const DUPE2 = 3
const SUIT = 15
const XFACTOR = 16
const PRIME = 12
const TRAGEDY = 14
const KILLING = 18
const EMPEROR = 19
const BAD = 20

const monde = () =>
  tableAvec(
    siege({
      area_hero: [
        carteSurTable(MM, 'mm001a', 'Hero', 'Multiple Man'),
        carteSurTable(SUIT, 'mm015', 'Upgrade', 'Kinetic Absorption Suit', { bind_object_id: MM }),
      ],
      allies: [carteSurTable(DUPE1, 'mm002', 'Ally', 'Dupe'), carteSurTable(DUPE2, 'mm003', 'Ally', 'Dupe')],
      supports: [carteSurTable(XFACTOR, 'mm016', 'Support', 'X-Factor Investigations')],
      engaged_enemies: [carteSurTable(EMPEROR, 'mm019', 'Minion', 'Emperor Madrox'), carteSurTable(BAD, 'mm020', 'Minion', 'Dupes Gone Bad')],
    }),
    {
      area_schemes_side: [
        carteSurTable(PRIME, 'mm012', 'PlayerSideScheme', 'Madrox Prime'),
        carteSurTable(TRAGEDY, 'mm014', 'PlayerSideScheme', 'Prepare For Future Tragedy'),
        carteSurTable(KILLING, 'mm018', 'SideScheme', "Who's Killing Dupes?"),
      ],
    },
  )

describe('Multiple Man : ce que la table dessine', () => {
  it("dessine Multiple Man, son costume (porté par l'identité), les deux Dupe (même nom, deux cartes) et X-Factor Investigations", () => {
    for (const id of [MM, SUIT, DUPE1, DUPE2, XFACTOR]) expect(dessinee(monde(), id)).toBeDefined()
    expect(dessinee(monde(), SUIT)?.portePar).toBe(MM)
    expect(dessinee(monde(), DUPE1)?.codeCarte).toBe('mm002')
    expect(dessinee(monde(), DUPE2)?.codeCarte).toBe('mm003')
  })
  it('dessine Emperor Madrox et Dupes Gone Bad engagés, et les trois manigances annexes (deux joueur, une de rencontre)', () => {
    for (const id of [EMPEROR, BAD, PRIME, TRAGEDY, KILLING]) expect(dessinee(monde(), id)).toBeDefined()
    expect(dessinee(monde(), EMPEROR)?.codeCarte).toBe('mm019')
  })
})
