// Hellfire Hunt, scenario 4 « Torn » : le deck Hellfire (sbires ELITE HELLFIRE, `cards.pack.hellfire_hunt_torn.DeckHellfire`) est un « deck supplementaire » du
// moteur (additional_decks), sa defausse une `additional_discard_piles`. Quand TOUTES leurs cartes portent les traits ELITE et HELLFIRE (cles `t_ELITE`, `t_HELLFIRE`
// du descripteur), la table les pose SOUS le deck et la defausse de rencontre (zone `piles-rencontre`) sous les titres « Deck Hellfire » / « Défausse Hellfire »,
// au lieu de les fondre dans « Cartes cachees » / « Cartes visibles » (zone `annexes`) ou ils se melangeraient au deck Recruited Mutants.
import { describe, expect, it } from 'vitest'
import { construirePlateau } from './zones'
import { catalogueVide } from './catalogue'
import { carteSurTable as carte, cartesDessinees, siege, tableAvec } from './plateau-de-test'
import type { World } from './world'

const elite = (id: number, code: string) => carte(id, code, 'Minion', 'Elite', { traits: { t_ELITE: 1, t_HELLFIRE: 1 }, is_face_up: false, visible_for_players: [] })
const recrute = (id: number) => carte(id, 'hf013', 'Ally', 'Armor', { traits: { t_MUTANT: 1, t_RECRUITED: 1 }, is_face_up: false, visible_for_players: [] })

const zones = (m: World) => cartesDessinees(m).map((c) => c.zone)
const plateau = (m: World) => JSON.stringify(construirePlateau(m, { playerId: 0, catalogue: catalogueVide }))

describe('deck Hellfire sur la table', () => {
  it('pose le deck Hellfire sous le deck de rencontre, sous son nom', () => {
    const m = tableAvec(siege(), { additional_decks: [[elite(1, 'hf341'), elite(2, 'hf351')]], additional_discard_piles: [[]] } as Partial<World>)
    expect(zones(m)).toContain('piles-rencontre')
    expect(zones(m)).not.toContain('annexes')
    expect(plateau(m)).toContain('hellfire-deck-0')   // la pile du deck Hellfire existe (son titre ne s'affiche que sur une pile regardable : comme le paquet de pieges)
  })
  it('pose la defausse Hellfire (non vide) au meme endroit, regardable, sous son nom', () => {
    const m = tableAvec(siege(), { additional_decks: [[elite(1, 'hf341')]], additional_discard_piles: [[elite(3, 'hf301')]] } as Partial<World>)
    expect(plateau(m)).toContain('Défausse Hellfire')
    expect(zones(m).filter((z) => z === 'piles-rencontre').length).toBe(2)
  })
  it('laisse le deck Recruited Mutants (allies RECRUITED) dans la pile des cartes cachees, a cote du deck Hellfire', () => {
    const m = tableAvec(siege(), { additional_decks: [[recrute(4)], [elite(1, 'hf341')]], additional_discard_piles: [[], []] } as Partial<World>)
    expect(zones(m)).toContain('annexes')
    expect(zones(m)).toContain('piles-rencontre')
  })
  it('laisse tout autre deck supplementaire dans la pile des cartes cachees', () => {
    const m = tableAvec(siege(), { additional_decks: [[recrute(4)]], additional_discard_piles: [[]] } as Partial<World>)
    expect(zones(m)).not.toContain('piles-rencontre')
    expect(zones(m)).toContain('annexes')
  })
})
