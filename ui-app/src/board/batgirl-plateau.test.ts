// Batgirl (`bg`, ES) : ce que le plateau DESSINE (PROCESSUS-CARTE étape 8 bis).
//
//  - bg011 Grapple Line : un compteur « recon » posé APRÈS l'attachement au héros doit se voir sur la carte ;
//  - bg015 Black Mask : sbire engagé avec le joueur, dessiné avec la manigance d'annexe bg014 (Return of the Mask) ;
//  - la carte rencontre donnée face cachée par Black Mask à SCH 0 n'a PAS de dessin propre (elle est dans la zone de cartes
//    rencontre données au siège, déjà couverte par les tests de `Puzzle.Deal`) : aucun cas ajouté pour elle.
// Modèle : attachement-en-chaine.test.ts (l'assertion qui compte est `toBeDefined()`).
import { describe, expect, it } from 'vitest'
import { carteSurTable, dessinee, siege, tableAvec } from './plateau-de-test'

const HEROS = 1
const GRAPPLE = 40
const MASQUE = 50
const MANIGANCE = 51

const monde = () =>
  tableAvec(
    siege({
      area_hero: [
        carteSurTable(HEROS, 'bg001a', 'Hero', 'Batgirl'),
        carteSurTable(GRAPPLE, 'bg011', 'Upgrade', 'Grapple Line', { bind_object_id: HEROS, info: { c_recon: 1 } }),
      ],
      engaged_enemies: [carteSurTable(MASQUE, 'bg015', 'Minion', 'Black Mask')],
    }),
    { area_schemes_side: [carteSurTable(MANIGANCE, 'bg014', 'SideScheme', 'Return of the Mask')] }
  )

describe('bg011 Grapple Line : compteur recon', () => {
  it('la carte est dessinée dans l unité du héros', () => {
    expect(dessinee(monde(), GRAPPLE)?.portePar).toBe(HEROS)
  })

  it('le compteur recon est dessiné avec sa valeur', () => {
    const compteurs = dessinee(monde(), GRAPPLE)?.compteurs ?? {}
    expect(compteurs['recon'] ?? compteurs['reconnaissance']).toBe(1)
  })
})

describe('bg015 Black Mask et bg014 Return of the Mask', () => {
  it('le sbire est dessiné', () => {
    expect(dessinee(monde(), MASQUE)).toBeDefined()
  })

  it('la manigance d annexe est dessinée', () => {
    expect(dessinee(monde(), MANIGANCE)).toBeDefined()
  })
})
