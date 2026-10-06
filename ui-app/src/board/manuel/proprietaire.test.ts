import { describe, expect, it } from 'vitest'
import { peutBouger, proprietaireDe, siegesControles } from './proprietaire'
import { carteSurTable, siege, tableAvec } from '../plateau-de-test'
import type { World } from '../world'

const MAIN_0 = carteSurTable(10, '01002', 'Ally', 'Allié du siège 0')
const DECK_1 = carteSurTable(11, '01003', 'Event', 'Carte du siège 1')
const SOUTIEN_1 = carteSurTable(12, '01006', 'Support', 'Soutien du siège 1')
const SBIRE_1 = carteSurTable(13, '01090', 'Minion', 'Sbire engagé avec le siège 1')
const VILAIN = carteSurTable(7, '01094', 'Villain', 'Rhino')

function monde(): World {
  const table = tableAvec(siege({ hand_cards: [MAIN_0] }), { villains: [VILAIN] } as never)
  return {
    ...table,
    players: [...table.players, siege({ player_deck: [DECK_1], supports: [SOUTIEN_1], engaged_enemies: [SBIRE_1] })],
  } as World
}

describe('à qui est une carte (lot 5, question 14)', () => {
  it('une carte de la main, du deck ou du jeu d un joueur est à son siège', () => {
    expect(proprietaireDe(monde(), MAIN_0.id)).toBe(0)
    expect(proprietaireDe(monde(), DECK_1.id)).toBe(1)
    expect(proprietaireDe(monde(), SOUTIEN_1.id)).toBe(1)
  })

  it('une carte Rencontre est à tous, même engagée avec un joueur', () => {
    expect(proprietaireDe(monde(), SBIRE_1.id)).toBeUndefined()
    expect(proprietaireDe(monde(), VILAIN.id)).toBeUndefined()
  })

  it('une carte inconnue n est à personne', () => {
    expect(proprietaireDe(monde(), 999)).toBeUndefined()
    expect(proprietaireDe(undefined, 10)).toBeUndefined()
  })
})

describe('qui peut la bouger', () => {
  it('à une même table (un seul écran), tous les sièges sont à moi', () => {
    expect(siegesControles(monde(), 0, false)).toEqual([0, 1])
  })

  it('en ligne, seulement mon siège', () => {
    expect(siegesControles(monde(), 1, true)).toEqual([1])
  })

  it('en ligne, mes cartes et les cartes Rencontre, jamais celles d un autre', () => {
    const miens = siegesControles(monde(), 0, true)
    expect(peutBouger(monde(), MAIN_0.id, miens)).toBe(true)
    expect(peutBouger(monde(), SBIRE_1.id, miens)).toBe(true)
    expect(peutBouger(monde(), VILAIN.id, miens)).toBe(true)
    expect(peutBouger(monde(), DECK_1.id, miens)).toBe(false)
    expect(peutBouger(monde(), SOUTIEN_1.id, miens)).toBe(false)
  })
})
