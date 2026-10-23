import { act, cleanup, render } from '@testing-library/react'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { CoucheChoixUniques, DUREE_BULLE_CHOIX_UNIQUE, phraseChoixUnique } from './choix-uniques'
import type { ChoixUnique } from './world'

const kelly: ChoixUnique = {
  id: 1,
  carte_id: 59,
  carte_code: '32069',
  carte: 'Sabretooth Strikes',
  option: 'Deal 1 damage to Robert Kelly',
  joueur: 0,
}

describe('phraseChoixUnique', () => {
  it('dit la carte, que l option etait seule, et ce qui a ete applique', () => {
    expect(phraseChoixUnique(kelly)).toBe(
      'Sabretooth Strikes : une seule option possible, appliquée d’office : Deal 1 damage to Robert Kelly'
    )
  })
})

describe('CoucheChoixUniques', () => {
  beforeEach(() => vi.useFakeTimers())
  afterEach(() => {
    cleanup()
    vi.useRealTimers()
  })

  it('ne rejoue pas les choix deja la au chargement', () => {
    render(<CoucheChoixUniques choix={[kelly]} />)
    expect(document.querySelector('.bulle-choix-unique')).toBeNull()
  })

  it('annonce un choix nouveau, puis l efface', () => {
    const { rerender } = render(<CoucheChoixUniques choix={[]} />)
    rerender(<CoucheChoixUniques choix={[kelly]} />)
    expect(document.querySelector('.bulle-choix-unique')?.textContent).toContain('une seule option possible')
    act(() => {
      vi.advanceTimersByTime(DUREE_BULLE_CHOIX_UNIQUE + 10)
    })
    expect(document.querySelector('.bulle-choix-unique')).toBeNull()
  })

  it('n annonce pas deux fois le meme choix', () => {
    const { rerender } = render(<CoucheChoixUniques choix={[]} />)
    rerender(<CoucheChoixUniques choix={[kelly]} />)
    act(() => {
      vi.advanceTimersByTime(DUREE_BULLE_CHOIX_UNIQUE + 10)
    })
    rerender(<CoucheChoixUniques choix={[kelly]} />)
    expect(document.querySelector('.bulle-choix-unique')).toBeNull()
  })
})
