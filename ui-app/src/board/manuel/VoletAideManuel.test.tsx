// @vitest-environment jsdom
import { describe, expect, it, vi } from 'vitest'
import { fireEvent, render, screen } from '@testing-library/react'
import { VoletAideManuel } from './VoletAideManuel'

describe('l’aide du mode manuel', () => {
  it('ouvert : liste les raccourcis OCTGN et les nôtres', () => {
    render(<VoletAideManuel ouvert ouvrir={() => {}} fermer={() => {}} />)
    const aide = screen.getByRole('dialog', { name: 'Aide du mode manuel' })
    for (const texte of ['Suppr', 'Double-clic', 'Maj + 1 à 9', 'Retourner la carte', 'Mélanger']) {
      expect(aide.textContent).toContain(texte)
    }
    expect(aide.textContent).toContain('C')
  })

  it('la croix ferme, la languette rouvre', () => {
    const fermer = vi.fn()
    const ouvrir = vi.fn()
    const { rerender } = render(<VoletAideManuel ouvert ouvrir={ouvrir} fermer={fermer} />)
    fireEvent.click(screen.getByTitle('Fermer'))
    expect(fermer).toHaveBeenCalledTimes(1)
    rerender(<VoletAideManuel ouvert={false} ouvrir={ouvrir} fermer={fermer} />)
    expect(screen.queryByRole('dialog')).toBeNull()
    fireEvent.click(screen.getByRole('button', { name: 'Aide' }))
    expect(ouvrir).toHaveBeenCalledTimes(1)
  })
})
