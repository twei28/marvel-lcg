// Sunspot (`so`, Dipsome, campagne Hellfire Hunt) : ce que le plateau DESSINE (PROCESSUS-CARTE étape 8 bis).
//
//  - le stock de compteurs « solar » vit sur l'IDENTITÉ (so001a/b) : il doit se voir sur la carte, avec sa valeur ;
//  - so010 Radiant Avenger et so011 Solar Soar sont des améliorations attachées au héros : elles doivent être dessinées dans son unité ;
//  - so013 Superhuman Mutants Murdering (manigance d'annexe) et so014 Donald Pierce (sbire engagé) sont dessinés.
// Modèle : batgirl-plateau.test.ts, attachement-en-chaine.test.ts (l'assertion qui compte est `toBeDefined()`).
import { describe, expect, it } from 'vitest'
import { carteSurTable, dessinee, siege, tableAvec } from './plateau-de-test'

const HEROS = 1
const AVENGER = 40
const SOAR = 41
const PIERCE = 50
const MANIGANCE = 51

const monde = () =>
  tableAvec(
    siege({
      area_hero: [
        carteSurTable(HEROS, 'so001a', 'Hero', 'Sunspot', { info: { c_solar: 5 } }),
        carteSurTable(AVENGER, 'so010', 'Upgrade', 'Radiant Avenger', { bind_object_id: HEROS }),
        carteSurTable(SOAR, 'so011', 'Upgrade', 'Solar Soar', { bind_object_id: HEROS }),
      ],
      engaged_enemies: [carteSurTable(PIERCE, 'so014', 'Minion', 'Donald Pierce')],
    }),
    { area_schemes_side: [carteSurTable(MANIGANCE, 'so013', 'SideScheme', 'Superhuman Mutants Murdering')] }
  )

describe('so001a Sunspot : le stock de compteurs solaires', () => {
  it('le compteur solar est dessiné sur le héros avec sa valeur', () => {
    const compteurs = dessinee(monde(), HEROS)?.compteurs ?? {}
    expect(compteurs['solar'] ?? compteurs['solaire']).toBe(5)
  })
})

describe('so010 Radiant Avenger et so011 Solar Soar : améliorations du héros', () => {
  it('Radiant Avenger est dessinée dans l unité du héros', () => {
    expect(dessinee(monde(), AVENGER)?.portePar).toBe(HEROS)
  })

  it('Solar Soar est dessinée dans l unité du héros', () => {
    expect(dessinee(monde(), SOAR)?.portePar).toBe(HEROS)
  })
})

describe('so013 et so014 : la némésis de Sunspot', () => {
  it('Donald Pierce est dessiné', () => {
    expect(dessinee(monde(), PIERCE)).toBeDefined()
  })

  it('la manigance d annexe est dessinée', () => {
    expect(dessinee(monde(), MANIGANCE)).toBeDefined()
  })
})
