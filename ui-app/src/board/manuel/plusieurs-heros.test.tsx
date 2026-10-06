// plusieurs-heros.test.tsx — lot 5 du 06/10/2026 : à plusieurs héros, chaque
// carte arrive chez son propriétaire, F12 et Ctrl+Q valent pour tous les héros
// de l'écran (question 7), et en ligne on ne touche pas aux cartes d'un autre
// (question 14). Harnais de clavier-wiring.test.tsx.
import { act, fireEvent, render, screen } from '@testing-library/react'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { CoucheTriche, useTriche } from '../CoucheTriche'
import { carteSurTable, siege, tableAvec } from '../plateau-de-test'
import type { World } from '../world'

const HEROS_0 = carteSurTable(1, '01001a', 'Hero', 'Spider-Man', { is_ready: false })
const HEROS_1 = carteSurTable(2, '01010a', 'Hero', 'Captain Marvel', { is_ready: false })
const DECK_0 = carteSurTable(30, '01002', 'Ally', 'Carte du deck 0')
const DECK_1 = carteSurTable(31, '01003', 'Ally', 'Carte du deck 1')
const SOUTIEN_1 = carteSurTable(32, '01006', 'Support', 'Soutien du siège 1')

function mondeADeux(): World {
  const table = tableAvec(
    siege({ area_hero: [HEROS_0], player_deck: [DECK_0], hand_size: 1, hand_cards: [] }),
    { mode_manuel: true, manuel_actif: true } as never
  )
  return {
    ...table,
    players: [
      ...table.players,
      siege({ area_hero: [HEROS_1], player_deck: [DECK_1], supports: [SOUTIEN_1], hand_size: 1, hand_cards: [] }),
    ],
  } as World
}

function Harness({ world, joueur, monSiege }: { world: World; joueur: number; monSiege: number }) {
  const triche = useTriche(world, joueur, undefined, monSiege)
  return <CoucheTriche actif={triche.actif} manuel={triche.manuel} couche={triche.couche} />
}

const commandes = () =>
  vi.mocked(fetch).mock.calls.flatMap(([, init]) => JSON.parse((init as RequestInit).body as string).commands as string[])

function survoler(id: number): HTMLElement {
  const noeud = document.createElement('div')
  noeud.setAttribute('data-card-id', String(id))
  document.body.appendChild(noeud)
  fireEvent.pointerMove(noeud)
  return noeud
}

beforeEach(() => {
  vi.stubGlobal('fetch', vi.fn(async () => ({ ok: true }) as Response))
})
afterEach(() => {
  window.history.replaceState(null, '', '/')
  document.body.innerHTML = ''
})

describe('à plusieurs héros, à la même table', () => {
  it('F12 redresse et fait piocher TOUS les héros, chacun dans sa main (question 7)', async () => {
    render(<Harness world={mondeADeux()} joueur={0} monSiege={0} />)
    fireEvent.keyDown(document, { key: 'F12' })
    await act(async () => { await Promise.resolve() })
    expect(commandes()).toEqual(
      expect.arrayContaining([
        'Puzzle.Ready(1)',
        'Puzzle.Ready(2)',
        'Puzzle.DrawUpToHandSize(siege=0)',
        'Puzzle.DrawUpToHandSize(siege=1)',
      ])
    )
    expect(commandes().some((c) => c.startsWith('Puzzle.Gain'))).toBe(false)
  })

  it('Ctrl+Q redresse tous les héros', async () => {
    render(<Harness world={mondeADeux()} joueur={0} monSiege={0} />)
    fireEvent.keyDown(document, { key: 'q', ctrlKey: true })
    await act(async () => { await Promise.resolve() })
    expect(commandes()).toEqual(expect.arrayContaining(['Puzzle.Ready(1)', 'Puzzle.Ready(2)']))
  })
})

describe('en ligne (question 14)', () => {
  beforeEach(() => {
    window.history.replaceState(null, '', '/?multi')
  })

  it('F12 ne vaut que pour mon héros', async () => {
    render(<Harness world={mondeADeux()} joueur={0} monSiege={0} />)
    fireEvent.keyDown(document, { key: 'F12' })
    await act(async () => { await Promise.resolve() })
    expect(commandes()).toContain('Puzzle.Ready(1)')
    expect(commandes()).not.toContain('Puzzle.Ready(2)')
  })

  it('le menu ne s’ouvre pas sur la carte d’un autre joueur', () => {
    render(<Harness world={mondeADeux()} joueur={1} monSiege={0} />)
    const noeud = survoler(SOUTIEN_1.id)
    fireEvent.contextMenu(noeud)
    expect(screen.queryByText('Incliner')).toBeNull()
  })

  it('une touche sur la carte d’un autre joueur n’envoie rien', async () => {
    render(<Harness world={mondeADeux()} joueur={1} monSiege={0} />)
    survoler(SOUTIEN_1.id)
    fireEvent.keyDown(document, { key: 'F7' })
    await act(async () => { await Promise.resolve() })
    expect(fetch).not.toHaveBeenCalled()
  })
})
