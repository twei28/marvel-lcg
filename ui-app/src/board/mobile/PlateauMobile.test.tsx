import { describe, expect, it } from 'vitest'
import { fireEvent, render, screen } from '@testing-library/react'
import { PlateauMobile } from './PlateauMobile'
import type { Plateau } from '../zones'
import type { World } from '../world'

// jsdom n'implemente pas ResizeObserver (aucune mise en page reelle). PlateauMobile
// en observe le cadre pour recalculer sa largeur de condensation : sans ce bouchon,
// tout rendu leverait une ReferenceError des le premier effet.
class ResizeObserverBouchon {
  observe() {}
  unobserve() {}
  disconnect() {}
}
;(globalThis as { ResizeObserver?: unknown }).ResizeObserver = ResizeObserverBouchon

const MONDE = {
  phase: 'Player 1 Turn',
  round_id: 3,
  prompt: '',
  players: [],
} as unknown as World

const PLATEAU: Plateau = {
  emplacements: [
    {
      cle: 'rencontre',
      titre: 'Méchant',
      nombreSurLaLigne: 1,
      groupes: [
        [
          {
            cle: 'v',
            carte: { id: '1', name: 'Rhino', kind: 'villain', imageUrl: '', allyHp: '12/22' },
            attachees: [],
          },
        ],
      ],
    },
  ],
  nombreDeCartes: 1,
  idsAffiches: new Set<number>([1]),
  representantsDePile: new Map<number, number>(),
  nombreIgnore: 0,
}

describe('PlateauMobile', () => {
  it('montre le HUD et les bandes peuplees', () => {
    render(
      <PlateauMobile world={MONDE} playerId={0} plateau={PLATEAU} source="test" />
    )
    expect(screen.getByText('Méchant')).toBeInTheDocument()
    expect(screen.getByText('Rhino')).toBeInTheDocument()
  })

  it('ne dessine aucune bande vide', () => {
    render(
      <PlateauMobile world={MONDE} playerId={0} plateau={PLATEAU} source="test" />
    )
    expect(screen.queryByText('Manigances')).not.toBeInTheDocument()
    expect(screen.queryByText('Ta main')).not.toBeInTheDocument()
  })

  it('ouvre la bande en focus au tap sur son titre', () => {
    render(
      <PlateauMobile world={MONDE} playerId={0} plateau={PLATEAU} source="test" />
    )
    fireEvent.click(screen.getByRole('button', { name: /Méchant/ }))
    expect(screen.getByRole('dialog', { name: 'Méchant' })).toBeInTheDocument()
  })
})
