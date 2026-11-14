// Batman (`bm`, ES) : ce que le plateau DESSINE (PROCESSUS-CARTE étape 8 bis).
//
//  - bm015 Two-Face : sbire némésis engagé avec le joueur, dessiné avec la manigance d'annexe bm014 (Split Decision) ;
//  - bm006 The Batcave : soutien en jeu ;
//  - bm009 Batsuit : amélioration attachée à l'identité, dessinée dans son unité ;
//  - le deck de dissuasion est le `additional_deck` du joueur, déjà dessiné comme « Special deck » (zones.ts) : aucune zone nouvelle,
//    aucun cas ajouté pour lui.
// Modèle : attachement-en-chaine.test.ts (l'assertion qui compte est `toBeDefined()`).
import { describe, expect, it } from 'vitest'
import { carteSurTable, dessinee, siege, tableAvec } from './plateau-de-test'

const HEROS = 1
const COSTUME = 40
const BATCAVE = 41
const DEUXFACE = 50
const MANIGANCE = 51

const monde = () =>
  tableAvec(
    siege({
      area_hero: [
        carteSurTable(HEROS, 'bm001a', 'Hero', 'Batman'),
        carteSurTable(COSTUME, 'bm009', 'Upgrade', 'Batsuit', { bind_object_id: HEROS }),
      ],
      supports: [carteSurTable(BATCAVE, 'bm006', 'Support', 'The Batcave')],
      engaged_enemies: [carteSurTable(DEUXFACE, 'bm015', 'Minion', 'Two-Face')],
    }),
    { area_schemes_side: [carteSurTable(MANIGANCE, 'bm014', 'SideScheme', 'Split Decision')] }
  )

describe('bm009 Batsuit : amélioration attachée', () => {
  it('la carte est dessinée dans l unité du héros', () => {
    expect(dessinee(monde(), COSTUME)?.portePar).toBe(HEROS)
  })
})

describe('bm006 The Batcave', () => {
  it('le soutien est dessiné', () => {
    expect(dessinee(monde(), BATCAVE)).toBeDefined()
  })
})

describe('bm015 Two-Face et bm014 Split Decision', () => {
  it('le sbire est dessiné', () => {
    expect(dessinee(monde(), DEUXFACE)).toBeDefined()
  })

  it('la manigance d annexe est dessinée', () => {
    expect(dessinee(monde(), MANIGANCE)).toBeDefined()
  })
})
