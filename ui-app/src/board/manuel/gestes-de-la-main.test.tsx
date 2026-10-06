// gestes-de-la-main.test.tsx — le menu de la main d'OCTGN (lot 6 du
// 06/10/2026) : défausse au hasard, mulligan, échange avec le dessus du deck.
// Chacun est UNE commande moteur (un seul Ctrl+Z). Harnais de
// clavier-wiring.test.tsx.
import { act, fireEvent, render, screen } from '@testing-library/react'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { CoucheTriche, useTriche } from '../CoucheTriche'
import { carteSurTable, siege, tableAvec } from '../plateau-de-test'
import type { World } from '../world'

const A = carteSurTable(30, '99002', 'Ally', 'Héliporteur')
const B = carteSurTable(31, '99003', 'Event', 'Uppercut')
const DECK = carteSurTable(40, '01004', 'Ally', 'Dessus du deck')

function monde(): World {
  return tableAvec(siege({ hand_cards: [A, B], player_deck: [DECK] }), { mode_manuel: true, manuel_actif: true } as never)
}

function Harness({ world }: { world: World }) {
  const triche = useTriche(world, 0)
  return <CoucheTriche actif={triche.actif} manuel={triche.manuel} couche={triche.couche} />
}

const commandes = () =>
  vi.mocked(fetch).mock.calls.flatMap(([, init]) => JSON.parse((init as RequestInit).body as string).commands as string[])

function clicDroitDansLeVide() {
  const vide = document.createElement('div')
  document.body.appendChild(vide)
  fireEvent.contextMenu(vide)
}

beforeEach(() => {
  vi.stubGlobal('fetch', vi.fn(async () => ({ ok: true }) as Response))
})
afterEach(() => {
  vi.restoreAllMocks()
  document.body.innerHTML = ''
})

describe('le menu de la main, comme OCTGN', () => {
  it('Mulligan : les cartes cochées partent, autant reviennent, en une commande', async () => {
    render(<Harness world={monde()} />)
    clicDroitDansLeVide()
    fireEvent.click(screen.getByText('Mulligan'))
    fireEvent.click(screen.getByRole('checkbox', { name: 'Héliporteur' }))
    fireEvent.click(screen.getByRole('checkbox', { name: 'Uppercut' }))
    fireEvent.click(screen.getByRole('button', { name: /Changer 2/ }))
    await act(async () => { await Promise.resolve() })
    expect(commandes()).toEqual(['Puzzle.Mulligan(30, 31, siege=0)'])
  })

  it('Défausser une carte au hasard', async () => {
    vi.spyOn(Math, 'random').mockReturnValue(0.99)
    render(<Harness world={monde()} />)
    clicDroitDansLeVide()
    fireEvent.click(screen.getByText('Défausser une carte au hasard'))
    await act(async () => { await Promise.resolve() })
    expect(commandes()).toEqual(["Puzzle.MoveTo(31, 'DiscardPile', 'Top', siege=0)"])
  })

  it('une carte de la main s’échange avec le dessus du deck', async () => {
    render(<Harness world={monde()} />)
    const noeud = document.createElement('div')
    noeud.setAttribute('data-card-id', '30')
    document.body.appendChild(noeud)
    fireEvent.contextMenu(noeud)
    fireEvent.click(screen.getByText('Échanger avec le dessus du deck'))
    await act(async () => { await Promise.resolve() })
    expect(commandes()).toEqual(['Puzzle.SwapWithDeckTop(30, siege=0)'])
  })

  it('l’échange n’est proposé que pour une carte de la main', () => {
    const avecAllie = tableAvec(siege({ hand_cards: [A], allies: [{ ...DECK, id: 41 }] }), {
      mode_manuel: true,
      manuel_actif: true,
    } as never)
    render(<Harness world={avecAllie} />)
    const noeud = document.createElement('div')
    noeud.setAttribute('data-card-id', '41')
    document.body.appendChild(noeud)
    fireEvent.contextMenu(noeud)
    expect(screen.queryByText('Échanger avec le dessus du deck')).toBeNull()
  })
})

// Lot 6 du 06/10/2026 : F12 complet, comme `doEndHeroPhase` d'OCTGN.
describe('F12 complet et fin du round', () => {
  it('F12 pioche jusqu’à la taille de main par une seule commande moteur', async () => {
    const plein = tableAvec(siege({ hand_cards: [A], player_deck: [DECK], hand_size: 3 }), {
      mode_manuel: true,
      manuel_actif: true,
    } as never)
    render(<Harness world={plein} />)
    fireEvent.keyDown(document, { key: 'F12' })
    await act(async () => { await Promise.resolve() })
    expect(commandes()).toContain('Puzzle.DrawUpToHandSize(siege=0)')
  })

  it('main trop grande : F12 propose de défausser l’excédent, en une commande', async () => {
    const tropPleine = tableAvec(siege({ hand_cards: [A, B], player_deck: [DECK], hand_size: 1 }), {
      mode_manuel: true,
      manuel_actif: true,
    } as never)
    render(<Harness world={tropPleine} />)
    fireEvent.keyDown(document, { key: 'F12' })
    await act(async () => { await Promise.resolve() })
    expect(commandes()).not.toContain('Puzzle.DrawUpToHandSize(siege=0)')
    fireEvent.click(screen.getByRole('checkbox', { name: 'Uppercut' }))
    fireEvent.click(screen.getByRole('button', { name: /Défausser 1/ }))
    await act(async () => { await Promise.resolve() })
    expect(commandes()).toContain('Puzzle.Discard(31)')
  })

  it('« Fin du round » au menu de la table : premier joueur suivant, round suivant', async () => {
    render(<Harness world={monde()} />)
    clicDroitDansLeVide()
    fireEvent.click(screen.getByText('Fin du round'))
    await act(async () => { await Promise.resolve() })
    expect(commandes()).toEqual(['Puzzle.EndRound()'])
  })
})
