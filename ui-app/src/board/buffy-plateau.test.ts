// Buffy (bf001a/b) : ce que la table DESSINE (étape 8 bis de PROCESSUS-CARTE).
//  - bf012 Redeemed s'attache à un sbire qui devient un allié : la carte attachée doit être dessinée, portée par son hôte ;
//  - bf027-bf032 (HELLMOUTH) : un complot annexe et un sbire révélés au Setup doivent être à l'écran ;
//  - bf014 Mr. Pointy est posé sur Buffy (héros).
import { describe, expect, it } from 'vitest'
import { carteSurTable, dessinee, siege, tableAvec } from './plateau-de-test'

const BUFFY = 1
const POINTY = 2
const ALLIE = 3
const REDEEMED = 4
const MASTER = 5
const HARVEST = 6

const monde = () =>
  tableAvec(
    siege({
      area_hero: [
        carteSurTable(BUFFY, 'bf001a', 'Hero', 'Buffy'),
        carteSurTable(POINTY, 'bf014', 'Upgrade', 'Mr. Pointy', { bind_object_id: BUFFY }),
      ],
      allies: [
        carteSurTable(ALLIE, '01101', 'Ally', 'Hydra Mercenary'),
        carteSurTable(REDEEMED, 'bf012', 'Upgrade', 'Redeemed', { bind_object_id: ALLIE }),
      ],
      engaged_enemies: [carteSurTable(MASTER, 'bf030', 'Minion', 'The Master')],
    }),
    { area_schemes_side: [carteSurTable(HARVEST, 'bf027', 'SideScheme', 'Harvest')] },
  )

describe('Buffy : ce que la table dessine', () => {
  it('dessine Mr. Pointy sur Buffy', () => {
    expect(dessinee(monde(), POINTY)).toBeDefined()
    expect(dessinee(monde(), POINTY)?.portePar).toBe(BUFFY)
  })
  it("dessine l'allié racheté et Redeemed qui lui est attachée", () => {
    expect(dessinee(monde(), ALLIE)).toBeDefined()
    expect(dessinee(monde(), REDEEMED)).toBeDefined()
    expect(dessinee(monde(), REDEEMED)?.portePar).toBe(ALLIE)
  })
  it('dessine The Master (engagé) et Harvest (complot annexe)', () => {
    expect(dessinee(monde(), MASTER)).toBeDefined()
    expect(dessinee(monde(), HARVEST)).toBeDefined()
  })
})
