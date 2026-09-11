import { fireEvent, render, screen } from '@testing-library/react'
import { describe, expect, it, vi } from 'vitest'
import { OngletsJoueurs } from './OngletsJoueurs'

describe('OngletsJoueurs', () => {
  it('ne montre RIEN en solo : un onglet unique est du bruit', () => {
    const { container } = render(
      <OngletsJoueurs joueurs={[{ id: 0, nom: 'Steve Rogers' }]} actif={0} choisir={() => {}} />
    )
    expect(container.firstChild).toBeNull()
  })

  it('un onglet par heros, celui qu on regarde est marque', () => {
    render(
      <OngletsJoueurs
        joueurs={[{ id: 0, nom: 'Steve Rogers' }, { id: 1, nom: 'Hulk' }]}
        actif={1}
        choisir={() => {}}
      />
    )
    expect(screen.getByRole('tab', { name: 'Hulk' })).toHaveAttribute('aria-selected', 'true')
    expect(screen.getByRole('tab', { name: 'Steve Rogers' })).toHaveAttribute('aria-selected', 'false')
  })

  it('taper un onglet change de joueur', () => {
    const choisir = vi.fn()
    render(
      <OngletsJoueurs
        joueurs={[{ id: 0, nom: 'Steve Rogers' }, { id: 1, nom: 'Hulk' }]}
        actif={0}
        choisir={choisir}
      />
    )
    fireEvent.click(screen.getByRole('tab', { name: 'Hulk' }))
    expect(choisir).toHaveBeenCalledWith(1)
  })
})
