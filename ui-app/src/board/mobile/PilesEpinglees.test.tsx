import { describe, expect, it, vi } from 'vitest'
import { fireEvent, render, screen } from '@testing-library/react'
import { PilesEpinglees } from './PilesEpinglees'
import type { UniteAffichee } from '../zones'

const deck: UniteAffichee = {
  cle: 'deck',
  carte: { id: '10', name: 'Encounter deck', kind: 'villain', imageUrl: '', facedown: true, pileCount: 23 },
  attachees: [],
  pileTitre: 'Deck de rencontre',
}

const defausse: UniteAffichee = {
  cle: 'defausse',
  carte: { id: '11', name: 'Advance', kind: 'treachery', imageUrl: '', discard: true },
  attachees: [],
  pileTitre: 'Défausse',
  pileContenu: [
    { id: '11', name: 'Advance', kind: 'treachery', imageUrl: '' },
    { id: '12', name: 'Assault', kind: 'treachery', imageUrl: '' },
  ],
}

describe('PilesEpinglees', () => {
  it('montre chaque pile avec son compte et son nom', () => {
    render(<PilesEpinglees piles={[deck, defausse]} onOuvrirPile={() => {}} />)
    expect(screen.getByText('23')).toBeInTheDocument()
    expect(screen.getByText('Deck de rencontre')).toBeInTheDocument()
    // Sans pileCount, le compte est la taille du contenu.
    expect(screen.getByText('2')).toBeInTheDocument()
    expect(document.querySelectorAll('[data-tactile="pile"]')).toHaveLength(2)
  })

  it('etale une pile consultable au tap, avec son titre', () => {
    const ouvrir = vi.fn()
    render(<PilesEpinglees piles={[deck, defausse]} onOuvrirPile={ouvrir} />)
    fireEvent.click(screen.getByRole('button', { name: /Défausse/ }))
    expect(ouvrir).toHaveBeenCalledWith('Défausse', defausse.pileContenu)
  })

  it('ne fait rien sur une pile secrete, et le dit', () => {
    const ouvrir = vi.fn()
    render(<PilesEpinglees piles={[deck]} onOuvrirPile={ouvrir} />)
    const pile = screen.getByRole('button', { name: /Deck de rencontre/ })
    expect(pile).toHaveAttribute('aria-disabled', 'true')
    fireEvent.click(pile)
    expect(ouvrir).not.toHaveBeenCalled()
  })
})
