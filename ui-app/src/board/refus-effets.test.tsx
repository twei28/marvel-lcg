import { act, cleanup, render } from '@testing-library/react'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { CoucheRefusEffets, DUREE_BULLE_REFUS, phraseRefusEffet } from './refus-effets'
import type { RefusEffet } from './world'

const lance: RefusEffet = {
  n: 1,
  genre: 'statut',
  statut: 'Stunned',
  motif: 'robuste',
  cible_id: 98,
  cible: 'Drang',
  cible_code: '16058',
  source: "Drang's Spear",
  source_code: '16064',
}

describe('phraseRefusEffet', () => {
  it('Robuste, avec la carte responsable', () => {
    expect(phraseRefusEffet(lance)).toMatch(/^Pas sonné : Robuste \(.+\)$/)
  })

  it('sans source quand Robuste est imprimé sur la carte elle-même', () => {
    expect(phraseRefusEffet({ ...lance, source: 'Drang', source_code: '16058' })).toBe('Pas sonné : Robuste')
  })

  it('déjà sonné', () => {
    expect(phraseRefusEffet({ ...lance, motif: 'deja', source: '', source_code: '' })).toBe('Pas sonné : déjà sonné')
  })
})

describe('CoucheRefusEffets', () => {
  beforeEach(() => vi.useFakeTimers())
  afterEach(() => {
    cleanup()
    vi.useRealTimers()
  })

  it('ne rejoue pas les refus déjà là au chargement', () => {
    render(<CoucheRefusEffets refus={[lance]} />)
    expect(document.querySelector('.bulle-refus-effet')).toBeNull()
  })

  it('montre un nouveau refus, puis l’efface', () => {
    const { rerender } = render(<CoucheRefusEffets refus={[]} />)
    rerender(<CoucheRefusEffets refus={[lance]} />)
    expect(document.querySelector('.bulle-refus-effet')?.textContent).toContain('Pas sonné : Robuste')
    act(() => {
      vi.advanceTimersByTime(DUREE_BULLE_REFUS + 10)
    })
    expect(document.querySelector('.bulle-refus-effet')).toBeNull()
  })

  it('une numérotation qui repart plus bas (annulation) ne montre rien d’ancien', () => {
    const { rerender } = render(<CoucheRefusEffets refus={[{ ...lance, n: 5 }]} />)
    rerender(<CoucheRefusEffets refus={[{ ...lance, n: 2 }]} />)
    expect(document.querySelector('.bulle-refus-effet')).toBeNull()
    rerender(<CoucheRefusEffets refus={[{ ...lance, n: 2 }, { ...lance, n: 3 }]} />)
    expect(document.querySelectorAll('.bulle-refus-effet')).toHaveLength(1)
  })
})
