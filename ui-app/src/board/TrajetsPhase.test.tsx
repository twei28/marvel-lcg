// Les trajets des cartes à l'écran (refonte, lot 4, essai, 12/10/2026).
import { act, render } from '@testing-library/react'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { TrajetsPhase } from './TrajetsPhase'

function carte(id: number, camp: 'player' | 'encounter' = 'encounter'): HTMLElement {
  const el = document.createElement('div')
  el.className = `scan-card camp-${camp}`
  el.dataset.cardId = String(id)
  const img = document.createElement('img')
  img.src = `/scan/${id}.jpg`
  el.append(img)
  return el
}

describe('les cartes volent vers la table et vers leur pile', () => {
  let table: HTMLElement
  beforeEach(() => {
    vi.stubGlobal('requestAnimationFrame', (cb: FrameRequestCallback) => window.setTimeout(() => cb(0), 0))
    vi.stubGlobal('cancelAnimationFrame', (n: number) => window.clearTimeout(n))
    vi.spyOn(HTMLElement.prototype, 'getBoundingClientRect').mockReturnValue({
      left: 10, top: 10, width: 100, height: 140, right: 110, bottom: 150, x: 10, y: 10, toJSON: () => ({}),
    } as DOMRect)
    ;(HTMLElement.prototype as unknown as { animate: unknown }).animate = vi.fn(() => ({ finish: vi.fn(), onfinish: null }))
    document.documentElement.removeAttribute('data-affichage')
    table = document.createElement('div')
    table.className = 'plateau-cadre'
    const boite = document.createElement('section')
    boite.className = 'deroule-phase est-essai'
    const pile = document.createElement('div')
    pile.dataset.pile = 'heros-0-defausse'
    table.append(boite, pile, carte(1, 'player'))
    document.body.append(table)
  })
  afterEach(() => {
    table.remove()
    document.querySelectorAll('.trajet-copie').forEach((e) => e.remove())
    vi.unstubAllGlobals()
    vi.restoreAllMocks()
  })

  it('une carte qui arrive : place en pointilles, une copie vole depuis la boite', async () => {
    render(<TrajetsPhase actif />)
    const nouvelle = carte(77)
    await act(async () => {
      table.append(nouvelle)
      await new Promise((r) => window.setTimeout(r, 250))
    })
    expect(nouvelle.classList.contains('trajet-arrivee')).toBe(true)
    expect(document.querySelectorAll('.trajet-copie')).toHaveLength(1)
  })

  it('une carte qui part : une copie vole vers sa pile', async () => {
    render(<TrajetsPhase actif />)
    await act(async () => {
      table.querySelector('[data-card-id="1"]')?.remove()
      await new Promise((r) => window.setTimeout(r, 250))
    })
    expect(document.querySelectorAll('.trajet-copie.est-depart')).toHaveLength(1)
  })

  it('un sbire qui arrive dans la rangee FONDUE des engages vole aussi ; une carte posee dans un deck, non', async () => {
    render(<TrajetsPhase actif />)
    const engages = document.createElement('div')
    engages.dataset.pile = 'terrain-combat-engages'
    const sbire = carte(57)
    engages.append(sbire)
    const deck = document.createElement('div')
    deck.dataset.pile = 'rencontre-encounter-deck'
    const dansLeDeck = carte(58)
    deck.append(dansLeDeck)
    await act(async () => {
      table.append(engages, deck)
      await new Promise((r) => window.setTimeout(r, 250))
    })
    expect(sbire.classList.contains('trajet-arrivee')).toBe(true)
    expect(dansLeDeck.classList.contains('trajet-arrivee')).toBe(false)
  })

  it('13/10/2026 : un dos distribué vole depuis le paquet rencontre, en dos', async () => {
    render(<TrajetsPhase actif />)
    const deck = document.createElement('div')
    deck.dataset.pile = 'rencontre-encounter-deck'
    const dos = carte(88)
    dos.classList.add('is-facedown')
    await act(async () => {
      table.append(deck, dos)
      await new Promise((r) => window.setTimeout(r, 250))
    })
    expect(dos.classList.contains('trajet-arrivee')).toBe(true)
    expect(document.querySelectorAll('.trajet-copie.est-dos')).toHaveLength(1)
  })

  it('13/10/2026 : un dos qui disparait (il est revele) ne part pas vers une defausse', async () => {
    const dos = carte(89)
    dos.classList.add('is-facedown')
    table.append(dos)
    render(<TrajetsPhase actif />)
    await act(async () => {
      dos.remove()
      await new Promise((r) => window.setTimeout(r, 250))
    })
    expect(document.querySelectorAll('.trajet-copie.est-depart')).toHaveLength(0)
  })

  it('en affichage sobre, rien ne vole', async () => {
    document.documentElement.setAttribute('data-affichage', 'sobre')
    render(<TrajetsPhase actif />)
    const nouvelle = carte(78)
    await act(async () => {
      table.append(nouvelle)
      await new Promise((r) => window.setTimeout(r, 250))
    })
    expect(nouvelle.classList.contains('trajet-arrivee')).toBe(false)
    expect(document.querySelectorAll('.trajet-copie')).toHaveLength(0)
  })

  it('inactif : rien ne vole', async () => {
    render(<TrajetsPhase actif={false} />)
    const nouvelle = carte(79)
    await act(async () => {
      table.append(nouvelle)
      await new Promise((r) => window.setTimeout(r, 250))
    })
    expect(document.querySelectorAll('.trajet-copie')).toHaveLength(0)
  })
})
