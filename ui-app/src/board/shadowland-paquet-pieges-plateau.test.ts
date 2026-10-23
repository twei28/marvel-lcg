// Shadowland, Shadow Labyrinth : le paquet de pieges est un « deck supplementaire » du moteur (additional_decks), sa defausse une
// `additional_discard_piles`. Quand TOUTES leurs cartes portent le trait TRAP (cle `t_TRAP` du descripteur, sans le « ! »), la table les pose
// SOUS le deck et la defausse de rencontre (zone `piles-rencontre`) au lieu de les fondre dans « Cartes cachees » (zone `annexes`).
import { describe, expect, it } from 'vitest'
import { construirePlateau } from './zones'
import { catalogueVide } from './catalogue'
import { carteSurTable as carte, cartesDessinees, siege, tableAvec } from './plateau-de-test'
import type { World } from './world'

const piege = (id: number, code: string) => carte(id, code, 'Treachery', 'Piege', { traits: { t_TRAP: 1 }, is_face_up: false, visible_for_players: [] })
const autre = (id: number) => carte(id, 'sl001a', 'MainScheme', 'Autre', { is_face_up: false, visible_for_players: [] })

const zones = (m: World) => cartesDessinees(m).map((c) => c.zone)

describe('paquet de pieges sur la table', () => {
  it('pose le paquet de pieges sous le deck de rencontre', () => {
    const m = tableAvec(siege(), { additional_decks: [[piege(1, 'sl050'), piege(2, 'sl051')]], additional_discard_piles: [[]] } as Partial<World>)
    expect(zones(m)).toContain('piles-rencontre')
    expect(zones(m)).not.toContain('annexes')
  })
  it('pose la defausse de pieges (non vide) au meme endroit, regardable, sous son nom', () => {
    const m = tableAvec(siege(), { additional_decks: [[piege(1, 'sl050')]], additional_discard_piles: [[piege(3, 'sl052')]] } as Partial<World>)
    const plateau = JSON.stringify(construirePlateau(m, { playerId: 0, catalogue: catalogueVide }))
    expect(plateau).toContain('Défausse de pièges')
    expect(zones(m).filter((z) => z === 'piles-rencontre').length).toBe(2)
  })
  it("laisse tout autre deck supplementaire dans la pile des cartes cachees", () => {
    const m = tableAvec(siege(), { additional_decks: [[autre(3)]], additional_discard_piles: [[]] } as Partial<World>)
    expect(zones(m)).not.toContain('piles-rencontre')
    expect(zones(m)).toContain('annexes')
  })
})
