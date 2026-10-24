import { beforeEach, describe, expect, it } from 'vitest'
import { fireEvent, render, screen } from '@testing-library/react'
import { CLES_TELEPHONE } from '../reglages-telephone'
import { VisiteGuidee, etapesDeLaVisite } from './VisiteGuidee'

describe('VisiteGuidee (Q57)', () => {
  beforeEach(() => window.localStorage.removeItem(CLES_TELEPHONE.aideDebut))
  it('compte 5 etapes', () => {
    expect(etapesDeLaVisite()).toHaveLength(5)
  })
  it('ne s\'ouvre pas tant que le jeu n\'est pas pret', () => {
    const { container } = render(<VisiteGuidee actif={false} />)
    expect(container.firstChild).toBeNull()
  })
  it('revient a la partie suivante tant que la case n\'est pas cochee', () => {
    const { unmount } = render(<VisiteGuidee actif />)
    for (let i = 0; i < 4; i++) fireEvent.click(screen.getByRole('button', { name: 'Suivant' }))
    fireEvent.click(screen.getByRole('button', { name: 'Terminer' }))
    expect(screen.queryByRole('dialog')).toBeNull()
    unmount()
    render(<VisiteGuidee actif />)
    expect(screen.getByRole('dialog')).toBeTruthy()
  })
  it('la case de la derniere etape coupe l\'aide pour les prochaines parties', () => {
    const { unmount } = render(<VisiteGuidee actif />)
    expect(screen.queryByRole('checkbox')).toBeNull()
    for (let i = 0; i < 4; i++) fireEvent.click(screen.getByRole('button', { name: 'Suivant' }))
    fireEvent.click(screen.getByRole('checkbox'))
    fireEvent.click(screen.getByRole('button', { name: 'Terminer' }))
    expect(window.localStorage.getItem(CLES_TELEPHONE.aideDebut)).toBe('non')
    unmount()
    const { container } = render(<VisiteGuidee actif />)
    expect(container.firstChild).toBeNull()
  })
  it('Passer ne la ferme que pour cette partie', () => {
    render(<VisiteGuidee actif />)
    fireEvent.click(screen.getByRole('button', { name: 'Passer' }))
    expect(screen.queryByRole('dialog')).toBeNull()
    expect(window.localStorage.getItem(CLES_TELEPHONE.aideDebut)).toBeNull()
  })
})
