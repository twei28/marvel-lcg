// Shadowland, Shadow Labyrinth : le paquet de pieges et sa defausse se montrent comme deux piles, a cote du deck de rencontre (23/10/2026).
// Le moteur les exporte sous `trap_deck` / `trap_discard_pile` ; absents hors de ce scenario.
import { describe, expect, it } from 'vitest'
import { carteSurTable as carte, cartesDessinees, siege, tableAvec } from './plateau-de-test'
import type { World } from './world'

const piege = (id: number, code: string) => carte(id, code, 'Treachery', 'Piege', { is_face_up: false, visible_for_players: [] })

describe('paquet de pieges sur la table', () => {
  it('montre deux piles quand le moteur les exporte', () => {
    const m = tableAvec(siege(), { trap_deck: [piege(1, 'sl050'), piege(2, 'sl051')], trap_discard_pile: [piege(3, 'sl052')] } as Partial<World>)
    const zones = cartesDessinees(m).filter((c) => c.zone === 'piles-rencontre').map((c) => c.id)
    expect(zones.length).toBeGreaterThanOrEqual(2)
  })
  it("n'ajoute aucune pile hors de Shadow Labyrinth", () => {
    const sans = cartesDessinees(tableAvec(siege())).filter((c) => c.zone === 'piles-rencontre').length
    const avec = cartesDessinees(tableAvec(siege(), { trap_deck: [], trap_discard_pile: [] } as Partial<World>)).filter((c) => c.zone === 'piles-rencontre').length
    expect(avec).toBe(sans)
  })
})
