// Mantis (mt001a/b) : ce que la table DESSINE (étape 8 bis de PROCESSUS-CARTE).
//  - mt008 Fortified Mind est attachée à Drax (mt002), un allié : la carte attachée doit être dessinée, portée par son hôte ;
//  - mt010 The Celestial Madonna est posée sur Mantis (héros) ;
//  - mt015 Cotati Resiliency est attachée à Plantman (mt014), sbire engagé ;
//  - mt012 Death Blossom's Bloom (complot annexe) est à l'écran.
import { describe, expect, it } from 'vitest'
import { carteSurTable, dessinee, siege, tableAvec } from './plateau-de-test'

const MANTIS = 1
const DRAX = 2
const FORTIFIED = 3
const MADONNA = 4
const PLANTMAN = 5
const COTATI = 6
const BLOOM = 7

const monde = () =>
  tableAvec(
    siege({
      area_hero: [
        carteSurTable(MANTIS, 'mt001a', 'Hero', 'Mantis'),
        carteSurTable(MADONNA, 'mt010', 'Upgrade', 'The Celestial Madonna', { bind_object_id: MANTIS }),
      ],
      allies: [
        carteSurTable(DRAX, 'mt002', 'Ally', 'Drax'),
        carteSurTable(FORTIFIED, 'mt008', 'Upgrade', 'Fortified Mind', { bind_object_id: DRAX }),
      ],
      engaged_enemies: [
        carteSurTable(PLANTMAN, 'mt014', 'Minion', 'Plantman'),
        carteSurTable(COTATI, 'mt015', 'Attachment', 'Cotati Resiliency', { bind_object_id: PLANTMAN }),
      ],
    }),
    { area_schemes_side: [carteSurTable(BLOOM, 'mt012', 'SideScheme', "Death Blossom's Bloom")] },
  )

describe('Mantis : ce que la table dessine', () => {
  it('dessine The Celestial Madonna sur Mantis', () => {
    expect(dessinee(monde(), MADONNA)).toBeDefined()
    expect(dessinee(monde(), MADONNA)?.portePar).toBe(MANTIS)
  })
  it("dessine Drax (allié) et Fortified Mind qui lui est attachée", () => {
    expect(dessinee(monde(), DRAX)).toBeDefined()
    expect(dessinee(monde(), FORTIFIED)).toBeDefined()
    expect(dessinee(monde(), FORTIFIED)?.portePar).toBe(DRAX)
  })
  it("dessine Plantman (engagé) et Cotati Resiliency qui lui est attachée", () => {
    expect(dessinee(monde(), PLANTMAN)).toBeDefined()
    expect(dessinee(monde(), COTATI)).toBeDefined()
    expect(dessinee(monde(), COTATI)?.portePar).toBe(PLANTMAN)
  })
  it("dessine Death Blossom's Bloom (complot annexe)", () => {
    expect(dessinee(monde(), BLOOM)).toBeDefined()
  })
})
