// @vitest-environment jsdom
import { describe, expect, it, vi } from 'vitest'
import { fireEvent, render, screen } from '@testing-library/react'
import { VoletAideManuel } from './VoletAideManuel'

describe('l’aide du mode manuel', () => {
  it('ouvert : liste les raccourcis d’OCTGN', () => {
    render(<VoletAideManuel ouvert ouvrir={() => {}} fermer={() => {}} />)
    const aide = screen.getByRole('dialog', { name: 'Aide du mode manuel' })
    for (const texte of ['Suppr', 'Double-clic', 'Clic droit sur la table', 'Défausser', 'Ctrl + F', 'F7', 'Alt + S', 'Ctrl + Alt + S', 'F4', 'Ctrl + Q', 'F12', 'Ctrl + Maj + D']) {
      expect(aide.textContent).toContain(texte)
    }
    expect(aide.textContent).toContain('Mélanger la pile')
  })

  it('explique d’abord comment jouer une carte (lot 3 du 06/10/2026)', () => {
    render(<VoletAideManuel ouvert ouvrir={() => {}} fermer={() => {}} />)
    const aide = screen.getByRole('dialog', { name: 'Aide du mode manuel' })
    for (const texte of ['Paie', 'Glisse la carte de ta main', 'Lâche sur une carte', 'Clic droit sur une carte', 'Poser en jeu']) {
      expect(aide.textContent).toContain(texte)
    }
    // Les noms officiels des statuts, comme sur les cartes françaises.
    for (const texte of ['Sonné', 'Désorienté', 'Tenace']) expect(aide.textContent).toContain(texte)
    for (const texte of ['Étourdi', 'Confus', 'Coriace']) expect(aide.textContent).not.toContain(texte)
    // Le clic droit sur la table, complet.
    for (const texte of ['Vaincre ce stade', 'Manigance terminée']) expect(aide.textContent).toContain(texte)
  })

  it('annonce les gestes du lot 6 et les touches maison (06/10/2026)', () => {
    render(<VoletAideManuel ouvert ouvrir={() => {}} fermer={() => {}} />)
    const aide = screen.getByRole('dialog', { name: 'Aide du mode manuel' })
    for (const texte of ['Ctrl + U', 'Maj + F1', 'F1', 'Q', 'R', 'Mulligan', 'Fin du round', 'face cachée', 'Échanger avec le dessus du deck']) {
      expect(aide.textContent).toContain(texte)
    }
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

describe('l’aide du mode manuel s’ouvre seule seulement sur PC (06/10/2026)', () => {
  const avecEcran = (requetesVraies: string[]) =>
    vi.spyOn(window, 'matchMedia').mockImplementation(
      (requete: string) =>
        ({ matches: requetesVraies.includes(requete), media: requete }) as unknown as MediaQueryList
    )

  it('sur PC (pointeur fin, 1100 px et plus), elle s’ouvre seule', async () => {
    const { aideSOuvreSeule } = await import('./VoletAideManuel')
    const espion = avecEcran([])
    expect(aideSOuvreSeule()).toBe(true)
    espion.mockRestore()
  })

  it('sur tablette ou téléphone, elle attend la languette', async () => {
    const { aideSOuvreSeule, ECRAN_SANS_AIDE_AUTO } = await import('./VoletAideManuel')
    const espion = avecEcran([ECRAN_SANS_AIDE_AUTO])
    expect(aideSOuvreSeule()).toBe(false)
    espion.mockRestore()
  })

  it('le critère couvre la largeur ET le pointeur grossier', async () => {
    const { ECRAN_SANS_AIDE_AUTO } = await import('./VoletAideManuel')
    expect(ECRAN_SANS_AIDE_AUTO).toBe('(max-width: 1099px), (pointer: coarse)')
  })
})
