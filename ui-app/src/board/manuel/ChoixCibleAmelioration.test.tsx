// La fenêtre « sur quelle carte ? » d'une amélioration lâchée sur la table
// (question 3 du 06/10/2026).
import { fireEvent, render } from '@testing-library/react'
import { describe, expect, it, vi } from 'vitest'
import { ChoixCibleAmelioration } from './ChoixCibleAmelioration'

const CHOIX = {
  sourceId: 42,
  nom: 'Web-Shooter',
  cibles: [
    { id: 1, nom: 'Spider-Man' },
    { id: 4, nom: 'Black Cat' },
  ],
}

describe('choisir la carte qui reçoit l’amélioration', () => {
  it('liste les cartes en jeu qui peuvent la recevoir, et rend celle choisie', () => {
    const onChoisir = vi.fn()
    const { getByRole } = render(<ChoixCibleAmelioration choix={CHOIX} onChoisir={onChoisir} onFermer={vi.fn()} />)
    expect(getByRole('dialog').textContent).toContain('Web-Shooter')
    expect(getByRole('button', { name: 'Spider-Man' })).toBeTruthy()
    fireEvent.click(getByRole('button', { name: 'Black Cat' }))
    expect(onChoisir).toHaveBeenCalledWith({ id: 4, nom: 'Black Cat' })
  })

  it('fermer sans choisir ne choisit rien (bouton, voile ou Échap)', () => {
    const onChoisir = vi.fn()
    const onFermer = vi.fn()
    const { getByRole, container } = render(
      <ChoixCibleAmelioration choix={CHOIX} onChoisir={onChoisir} onFermer={onFermer} />
    )
    fireEvent.click(getByRole('button', { name: 'Annuler' }))
    fireEvent.pointerDown(container.querySelector('.pile-triche-voile')!)
    fireEvent.keyDown(document, { key: 'Escape' })
    expect(onFermer).toHaveBeenCalledTimes(3)
    expect(onChoisir).not.toHaveBeenCalled()
  })
})
