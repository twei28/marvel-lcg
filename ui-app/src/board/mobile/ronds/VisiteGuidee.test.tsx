import { beforeEach, describe, expect, it } from 'vitest'
import { fireEvent, render, screen } from '@testing-library/react'
import { CLES_TELEPHONE, lireReglagesTelephone } from '../reglages-telephone'
import { VisiteGuidee, etapesDeLaVisite } from './VisiteGuidee'

describe('VisiteGuidee (Q57)', () => {
  beforeEach(() => {
    window.localStorage.removeItem(CLES_TELEPHONE.aideDebut)
    window.localStorage.removeItem(CLES_TELEPHONE.visitePiles)
  })
  it('compte 6 etapes : les 5 d\'origine dans leur ordre, puis les cartes empilees', () => {
    const titres = etapesDeLaVisite().map((e) => e.titre)
    expect(titres).toEqual(['Les ronds', 'Ta main', 'La phase', 'Glisser', 'Le menu', 'Cartes empilées'])
  })
  it('ne s\'ouvre pas tant que le jeu n\'est pas pret', () => {
    const { container } = render(<VisiteGuidee actif={false} />)
    expect(container.firstChild).toBeNull()
  })
  it('ne revient plus apres Terminer', () => {
    const { unmount } = render(<VisiteGuidee actif />)
    for (let i = 0; i < 5; i++) fireEvent.click(screen.getByRole('button', { name: 'Suivant' }))
    fireEvent.click(screen.getByRole('button', { name: 'Terminer' }))
    expect(window.localStorage.getItem(CLES_TELEPHONE.aideDebut)).toBe('non')
    expect(window.localStorage.getItem(CLES_TELEPHONE.visitePiles)).toBe('non')
    unmount()
    const { container } = render(<VisiteGuidee actif />)
    expect(container.firstChild).toBeNull()
  })
  it('Passer la ferme pour de bon aussi', () => {
    render(<VisiteGuidee actif />)
    fireEvent.click(screen.getByRole('button', { name: 'Passer' }))
    expect(screen.queryByRole('dialog')).toBeNull()
    expect(window.localStorage.getItem(CLES_TELEPHONE.aideDebut)).toBe('non')
    expect(window.localStorage.getItem(CLES_TELEPHONE.visitePiles)).toBe('non')
  })
  it('l\'etape des piles montre l\'exemple (contour pointille dore + pastille) et dit que ce n\'est pas une amelioration', () => {
    render(<VisiteGuidee actif />)
    for (let i = 0; i < 5; i++) fireEvent.click(screen.getByRole('button', { name: 'Suivant' }))
    const bulle = screen.getByRole('dialog')
    expect(bulle.textContent).toContain('6 / 6')
    expect(bulle.textContent).toContain('Pile de cartes')
    expect(bulle.textContent).toContain('pas une amélioration')
    expect(bulle.querySelector('.visite-pile-exemple .est-empilee')).not.toBeNull()
    expect(bulle.querySelector('.visite-pile-exemple .pile-sous-carte')).not.toBeNull()
  })
  it('un joueur qui a DEJA vu la visite ne voit que la nouveaute, une seule fois', () => {
    window.localStorage.setItem(CLES_TELEPHONE.aideDebut, 'non')
    const { unmount } = render(<VisiteGuidee actif />)
    const bulle = screen.getByRole('dialog')
    expect(bulle.textContent).toContain('Cartes empilées')
    expect(bulle.textContent).toContain('Nouveauté')
    expect(bulle.textContent).not.toContain('Les ronds')
    expect(screen.queryByRole('button', { name: 'Suivant' })).toBeNull()
    fireEvent.click(screen.getByRole('button', { name: 'Compris' }))
    expect(window.localStorage.getItem(CLES_TELEPHONE.visitePiles)).toBe('non')
    // La visite complete n'est pas relancee : le reglage « aide au debut » reste coupe.
    expect(lireReglagesTelephone().aideDebut).toBe(false)
    unmount()
    const { container } = render(<VisiteGuidee actif />)
    expect(container.firstChild).toBeNull()
  })
  it('un joueur qui a tout vu (visite et nouveaute) ne revoit rien', () => {
    window.localStorage.setItem(CLES_TELEPHONE.aideDebut, 'non')
    window.localStorage.setItem(CLES_TELEPHONE.visitePiles, 'non')
    const { container } = render(<VisiteGuidee actif />)
    expect(container.firstChild).toBeNull()
  })
  it('« Aide au debut de la partie » (reglages) relance la visite complete', () => {
    window.localStorage.setItem(CLES_TELEPHONE.aideDebut, 'oui')
    window.localStorage.setItem(CLES_TELEPHONE.visitePiles, 'non')
    render(<VisiteGuidee actif />)
    expect(screen.getByRole('dialog').textContent).toContain('1 / 6')
  })
})
