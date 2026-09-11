import { render, screen } from '@testing-library/react'
import { describe, expect, it, vi } from 'vitest'
import { PlateauMobile } from './PlateauMobile'
import type { BoardProps } from '../Board'

// `vi.mock` est hissé en tête de module : sa factory ne peut pas lire un
// `let` déclaré plus bas (ReferenceError, temporal dead zone). `vi.hoisted`
// crée la valeur mutable AVANT ce hissage, donc la factory peut la fermer.
const etat = vi.hoisted(() => ({ orientation: 'portrait' as 'portrait' | 'paysage' }))
vi.mock('./useOrientation', () => ({ useOrientation: () => etat.orientation }))

const props = {
  world: { render_id: 1, round_id: 1, phase: 'Player 1 Turn', players: [] },
  playerId: 0,
  plateau: { emplacements: [], nombreDeCartes: 0, idsAffiches: new Set(), representantsDePile: new Map(), nombreIgnore: 0 },
} as unknown as BoardProps

describe('le telephone ne joue qu en portrait', () => {
  it('monte le plateau portrait quand l ecran est debout', () => {
    etat.orientation = 'portrait'
    const { container } = render(<PlateauMobile {...props} />)
    expect(container.querySelector('.plateau-portrait')).not.toBeNull()
    expect(screen.queryByText(/remets ton/i)).toBeNull()
  })

  it('demande de remettre l ecran droit quand il est couche', () => {
    etat.orientation = 'paysage'
    render(<PlateauMobile {...props} />)
    expect(screen.getByText(/remets ton téléphone droit/i)).toBeInTheDocument()
  })
})
