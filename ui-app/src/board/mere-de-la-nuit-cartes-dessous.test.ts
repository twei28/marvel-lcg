// Les cartes glissées face cachée sous une MANIGANCE ANNEXE doivent être
// dessinées (étape 8 bis de PROCESSUS-CARTE, leçon Contingency Plan).
//
// The Mother of Night (`ze014`, set némésis de Zeus, 11/09/2026) cherche dans
// le deck et la défausse de chaque joueur deux cartes à énergie imprimée et
// les place face cachée sous elle : le moteur les émet dans `area_schemes_side`
// à la suite de la manigance, liées par `bind_object_id`. Même mécanisme que
// Highway Robbery (`01166`) : ce cas vaut donc pour les deux.
import { describe, expect, it } from 'vitest'
import { carteSurTable, cartesDessinees, dessinee, siege, tableAvec } from './plateau-de-test'

const MANIGANCE = 30
const THUNDERBOLT = 31
const WRATH = 32

const monde = () =>
  tableAvec(siege({ area_hero: [carteSurTable(1, 'ze001a', 'Hero', 'Zeus')] }), {
    area_schemes_side: [
      carteSurTable(MANIGANCE, 'ze014', 'SideScheme', 'The Mother of Night'),
      carteSurTable(THUNDERBOLT, 'ze008', 'Upgrade', 'Thunderbolt', {
        bind_object_id: MANIGANCE,
        is_face_up: false,
        visible_for_players: [],
      }),
      carteSurTable(WRATH, 'ze006', 'Event', 'Wrath of Olympus', {
        bind_object_id: MANIGANCE,
        is_face_up: false,
        visible_for_players: [],
      }),
    ],
  })

describe('The Mother of Night, cartes glissées dessous', () => {
  it('dessine la manigance annexe', () => {
    expect(dessinee(monde(), MANIGANCE)).toBeDefined()
  })

  it('dessine les deux cartes glissées, portées par la manigance', () => {
    expect(dessinee(monde(), THUNDERBOLT)).toBeDefined()
    expect(dessinee(monde(), WRATH)).toBeDefined()
    expect(dessinee(monde(), THUNDERBOLT)?.portePar).toBe(MANIGANCE)
    expect(dessinee(monde(), WRATH)?.portePar).toBe(MANIGANCE)
  })

  it('les montre face cachée, juste derrière la manigance', () => {
    const vues = cartesDessinees(monde())
    const rang = (id: number) => vues.findIndex((c) => c.id === id)
    expect(rang(THUNDERBOLT)).toBe(rang(MANIGANCE) + 1)
    expect(rang(WRATH)).toBe(rang(MANIGANCE) + 2)
    expect(dessinee(monde(), THUNDERBOLT)?.facedown).toBe(true)
  })
})
