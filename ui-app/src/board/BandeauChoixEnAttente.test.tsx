import { describe, expect, it, vi } from 'vitest'
import { fireEvent, render, screen } from '@testing-library/react'
import { BandeauChoixEnAttente } from './BandeauChoixEnAttente'

// Fenetre de choix fermee sans annuler (telephone) : un bandeau discret dit que le choix attend, et propose de rouvrir.
describe('BandeauChoixEnAttente', () => {
  it('dit « Choisis une carte » avec le nom de l’action, et rouvre au tap', () => {
    const rouvrir = vi.fn()
    render(<BandeauChoixEnAttente titre="Jouer En Costume" onRouvrir={rouvrir} />)
    expect(screen.getByRole('status').textContent).toContain('Choisis une carte')
    expect(screen.getByRole('status').textContent).toContain('Jouer En Costume')
    fireEvent.click(screen.getByRole('button', { name: 'Rouvrir' }))
    expect(rouvrir).toHaveBeenCalledOnce()
  })
})
