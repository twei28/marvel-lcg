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

describe('phraseChoixUnique, avis libre (Safe House #30, 26/10/2026)', () => {
  const sansSbire: ChoixUnique = {
    id: 2,
    carte_id: 70,
    carte_code: '54007',
    carte: 'Safe House #30',
    option: '',
    joueur: 0,
    texte: 'No minion in the encounter deck: no card is drawn.',
  }

  it('dit l avis du moteur, traduit, a la place de « une seule option possible »', () => {
    expect(phraseChoixUnique(sansSbire)).toBe('Safe House #30 : Aucun sbire dans le deck de rencontre : aucune carte n’est piochée.')
    expect(phraseChoixUnique(sansSbire)).not.toContain('une seule option possible')
  })

  it('garde l avis anglais du moteur quand le plateau est en anglais', () => {
    localStorage.setItem('marvel-langue', 'en')
    try {
      expect(phraseChoixUnique(sansSbire)).toBe('Safe House #30 : No minion in the encounter deck: no card is drawn.')
    } finally {
      localStorage.removeItem('marvel-langue')
    }
  })

  it('une bulle est annoncee pour un avis libre', () => {
    vi.useFakeTimers()
    const { rerender } = render(<CoucheChoixUniques choix={[]} />)
    rerender(<CoucheChoixUniques choix={[sansSbire]} />)
    expect(document.querySelector('.bulle-choix-unique')?.textContent).toContain('aucune carte')
    cleanup()
    vi.useRealTimers()
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
