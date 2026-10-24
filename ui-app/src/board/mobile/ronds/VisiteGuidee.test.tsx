import { beforeEach, describe, expect, it } from 'vitest'
import { fireEvent, render, screen } from '@testing-library/react'
import { CLE_VISITE_RONDS, VisiteGuidee, etapesDeLaVisite } from './VisiteGuidee'

describe('VisiteGuidee (Q57)', () => {
  beforeEach(() => window.localStorage.removeItem(CLE_VISITE_RONDS))
  it('compte 5 etapes', () => {
    expect(etapesDeLaVisite()).toHaveLength(5)
  })
  it('ne s\'ouvre pas tant que le jeu n\'est pas pret', () => {
    const { container } = render(<VisiteGuidee actif={false} />)
    expect(container.firstChild).toBeNull()
  })
  it('se deroule en 5 etapes puis ne revient plus', () => {
    const { unmount } = render(<VisiteGuidee actif />)
    expect(screen.getByText('1 / 5')).toBeTruthy()
    for (let i = 0; i < 4; i++) fireEvent.click(screen.getByRole('button', { name: 'Suivant' }))
    expect(screen.getByText('5 / 5')).toBeTruthy()
    fireEvent.click(screen.getByRole('button', { name: 'Terminer' }))
    expect(screen.queryByRole('dialog')).toBeNull()
    unmount()
    const { container } = render(<VisiteGuidee actif />)
    expect(container.firstChild).toBeNull()
  })
  it('Passer la ferme pour de bon', () => {
    render(<VisiteGuidee actif />)
    fireEvent.click(screen.getByRole('button', { name: 'Passer' }))
    expect(window.localStorage.getItem(CLE_VISITE_RONDS)).toBe('oui')
  })
})
