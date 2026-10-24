// La tablette (24/10/2026, decisions 3 a 5) : pas de survol ; un toucher ouvre l'apercu
// de la carte, qui reste ouvert avec la place des boutons dessous ; un toucher a cote le ferme.
import { act, fireEvent, render } from '@testing-library/react'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { Board } from '../Board'
import { catalogueVide } from '../catalogue'
import { carteSurTable as carte, siege, tableAvec } from '../plateau-de-test'
import { construirePlateau } from '../zones'

beforeEach(() => {
  vi.useFakeTimers()
  vi.stubGlobal('ResizeObserver', class { observe() {} unobserve() {} disconnect() {} })
})
afterEach(() => vi.useRealTimers())

function plateau() {
  const monde = tableAvec(siege({ area_hero: [carte(1, '01001b', 'AlterEgo', 'Peter Parker')], hand_cards: [carte(2, '01088', 'Event', 'Energie')] }))
  return { monde, plateau: construirePlateau(monde, { playerId: 0, catalogue: catalogueVide }) }
}

describe('apercu tenu de la tablette', () => {
  it('le survol ne montre rien, le toucher ouvre l apercu tenu, toucher a cote le ferme', () => {
    const { monde, plateau: p } = plateau()
    const rendu = render(<Board world={monde} playerId={0} plateau={p} bandeManigances tablette />)
    const heros = rendu.container.querySelector('[data-card-id="1"]')!
    fireEvent.mouseOver(heros)
    act(() => {
      vi.advanceTimersByTime(300)
    })
    expect(document.querySelector('.carte-apercu')).toBeNull()

    fireEvent.pointerUp(heros)
    expect(document.querySelector('.carte-apercu.est-tenu .apercu-actions-tablette')).not.toBeNull()

    fireEvent.pointerDown(document.body)
    expect(document.querySelector('.carte-apercu')).toBeNull()
  })

  it('sans tablette, le PC garde son survol', () => {
    const { monde, plateau: p } = plateau()
    const rendu = render(<Board world={monde} playerId={0} plateau={p} bandeManigances />)
    fireEvent.mouseOver(rendu.container.querySelector('[data-card-id="1"]')!)
    act(() => {
      vi.advanceTimersByTime(300)
    })
    expect(document.querySelector('.carte-apercu.est-tenu')).toBeNull()
    expect(document.querySelector('.carte-apercu')).not.toBeNull()
  })
})
