import { render } from '@testing-library/react'
import { afterEach, describe, expect, it } from 'vitest'
import { PlateauMobile } from './PlateauMobile'
import type { BoardProps } from '../Board'

const props = {
  world: { render_id: 1, round_id: 1, phase: 'Player 1 Turn', players: [] },
  playerId: 0,
  plateau: { emplacements: [], nombreDeCartes: 0, idsAffiches: new Set(), representantsDePile: new Map(), nombreIgnore: 0 },
} as unknown as BoardProps

describe('le rendu telephone', () => {
  afterEach(() => {
    document.body.classList.remove('mode-plateau-portrait')
  })

  it('monte le plateau en bandes, sans ecran « remets ton telephone droit » (meme plateau en paysage, spec du 12/09/2026)', () => {
    const { container } = render(<PlateauMobile {...props} />)
    expect(container.querySelector('.plateau-portrait')).not.toBeNull()
    expect(container.querySelectorAll('.bande')).toHaveLength(4)
    expect(container.querySelector('.ecran-paysage')).toBeNull()
  })

  it('pose la classe du plateau portrait sur body, et la retire au demontage', () => {
    const { unmount } = render(<PlateauMobile {...props} />)
    expect(document.body.classList.contains('mode-plateau-portrait')).toBe(true)
    unmount()
    expect(document.body.classList.contains('mode-plateau-portrait')).toBe(false)
  })
})
