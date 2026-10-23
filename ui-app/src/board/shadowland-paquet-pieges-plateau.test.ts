// Shadowland, Shadow Labyrinth : le paquet de pieges est un « deck supplementaire » du moteur (additional_decks) ; la pile des cartes cachees
// l'appelle « Paquet de pieges » quand toutes ses cartes portent le trait TRAP (cle `t_TRAP` dans le descripteur), sinon « Deck supplementaire ».
import { describe, expect, it } from 'vitest'
import { construirePlateau } from './zones'
import { catalogueVide } from './catalogue'
import { carteSurTable as carte, siege, tableAvec } from './plateau-de-test'
import type { World } from './world'

const piege = (id: number, code: string) => carte(id, code, 'Treachery', 'Piege', { traits: { t_TRAP: 1 }, is_face_up: false, visible_for_players: [] })

const titres = (m: World): string[] => {
  const plateau = construirePlateau(m, { playerId: 0, catalogue: catalogueVide })
  return JSON.stringify(plateau).match(/(Paquet de pièges|Deck supplémentaire \d)/g) ?? []
}

describe('paquet de pieges sur la table', () => {
  it('nomme « Paquet de pièges » un deck supplementaire fait de cartes TRAP', () => {
    const m = tableAvec(siege(), { additional_decks: [[piege(1, 'sl050'), piege(2, 'sl051')]], additional_discard_piles: [[]] } as Partial<World>)
    expect(titres(m)).toContain('Paquet de pièges')
  })
  it('garde « Deck supplémentaire » pour tout autre deck', () => {
    const m = tableAvec(siege(), { additional_decks: [[carte(3, 'sl001a', 'MainScheme', 'X')]], additional_discard_piles: [[]] } as Partial<World>)
    expect(titres(m)).not.toContain('Paquet de pièges')
  })
})
