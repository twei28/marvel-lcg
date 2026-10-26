// Smasher (Starjammers, sz001a) : ce que la table DESSINE (étape 8 bis de PROCESSUS-CARTE, leçon Contingency Plan).
//
// Une amélioration EXOSPEX se pose sur l'identité de Smasher (une seule à la fois, les autres sont défaussées), Cannonball est un allié
// qui peut porter une carte d'état Tough. Le moteur les émet à la suite de leur hôte,
// liés par `bind_object_id` (modèle `attachement-en-chaine.test.ts`) : une carte non dessinée serait invisible alors que sa règle s'applique.
import { describe, expect, it } from 'vitest'
import { carteSurTable, cartesDessinees, dessinee, siege, tableAvec } from './plateau-de-test'

const SMASHER = 1
const PENTA_VISION = 2
const CANNONBALL = 3
const HOME = 4

const monde = () =>
  tableAvec(
    siege({
      area_hero: [
        carteSurTable(SMASHER, 'sz001a', 'Hero', 'Smasher'),
        carteSurTable(PENTA_VISION, 'sz005', 'Upgrade', 'Penta-Vision', { bind_object_id: SMASHER }),
      ],
      allies: [carteSurTable(CANNONBALL, 'sz002', 'Ally', 'Cannonball')],
      supports: [carteSurTable(HOME, 'sz003', 'Support', 'Home on Chandilar')],
    }),
  )

describe('Smasher, amélioration EXOSPEX sur son identité', () => {
  it('dessine Smasher et Penta-Vision, portée par elle', () => {
    expect(dessinee(monde(), SMASHER)).toBeDefined()
    expect(dessinee(monde(), PENTA_VISION)?.portePar).toBe(SMASHER)
  })

  it('dessine Penta-Vision juste derrière Smasher', () => {
    const vues = cartesDessinees(monde())
    const rang = (id: number) => vues.findIndex((c) => c.id === id)
    expect(rang(PENTA_VISION)).toBe(rang(SMASHER) + 1)
  })
})

describe('Cannonball et Home on Chandilar', () => {
  it('dessine l\'allié Cannonball et le soutien Home on Chandilar', () => {
    expect(dessinee(monde(), CANNONBALL)).toBeDefined()
    expect(dessinee(monde(), HOME)).toBeDefined()
  })
})
