// L'annonce de la phase du mechant : un bandeau rouge qui traverse l'ecran.
//
// Il se raccourcit a partir du round 4 : deux secondes de solennite a chaque
// round d'une partie qui en compte douze finiraient par lasser.
import { describe, expect, it, vi, afterEach } from 'vitest'
import { render, act } from '@testing-library/react'
import { BandeauPhase, DUREE_LONGUE_MS, DUREE_COURTE_MS } from './BandeauPhase'

afterEach(() => {
  vi.useRealTimers()
})

describe('annonce de phase', () => {
  it('s affiche quand la phase commence', () => {
    const { container } = render(<BandeauPhase round={1} actif />)
    expect(container.querySelector('.bandeau-phase')).not.toBeNull()
  })

  it('ne s affiche pas hors phase', () => {
    const { container } = render(<BandeauPhase round={1} actif={false} />)
    expect(container.querySelector('.bandeau-phase')).toBeNull()
  })

  it('annonce le round', () => {
    const { container } = render(<BandeauPhase round={3} actif />)
    expect(container.textContent).toContain('3')
  })

  it('disparait de lui-meme', () => {
    vi.useFakeTimers()
    const { container } = render(<BandeauPhase round={1} actif />)
    act(() => {
      vi.advanceTimersByTime(DUREE_LONGUE_MS + 100)
    })
    expect(container.querySelector('.bandeau-phase')).toBeNull()
  })

  it('dure moins longtemps a partir du round 4', () => {
    vi.useFakeTimers()
    const { container } = render(<BandeauPhase round={4} actif />)
    act(() => {
      vi.advanceTimersByTime(DUREE_COURTE_MS + 100)
    })
    expect(container.querySelector('.bandeau-phase')).toBeNull()
  })

  it('tient encore la duree longue au round 3', () => {
    vi.useFakeTimers()
    const { container } = render(<BandeauPhase round={3} actif />)
    act(() => {
      vi.advanceTimersByTime(DUREE_COURTE_MS + 100)
    })
    expect(container.querySelector('.bandeau-phase')).not.toBeNull()
  })
})
