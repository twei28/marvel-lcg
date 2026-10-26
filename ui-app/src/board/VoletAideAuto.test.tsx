// @vitest-environment jsdom
import { afterEach, describe, expect, it } from 'vitest'
import { cleanup, render, screen } from '@testing-library/react'
import { VoletAideAuto } from './VoletAideAuto'
import { DICO_EN_BASE } from './dico-en'

afterEach(cleanup)

const rien = () => {}

describe('l’aide du mode auto', () => {
  it('sur PC : les touches du clavier et le glisser-Alt', () => {
    render(<VoletAideAuto ouvert ouvrir={rien} fermer={rien} />)
    const aide = screen.getByRole('dialog', { name: 'Aide' })
    // Les touches existantes sont toutes listees (E, Espace, U, B, chiffres, Échap).
    for (const texte of ['E  Espace', 'U', 'Copier le rapport de bug', '1 à 9', 'Choisir l’option portant ce numéro', 'Échap', 'Alt + glisser', 'Double-clic sur le titre']) expect(aide.textContent).toContain(texte)
    expect(aide.textContent).not.toContain('Languette de droite')
  })

  it('sur téléphone : les gestes du doigt, sans touche de clavier', () => {
    render(<VoletAideAuto ouvert ouvrir={rien} fermer={rien} telephone />)
    const aide = screen.getByRole('dialog', { name: 'Aide' })
    for (const texte of [
      'Le plateau',
      'Ta main',
      'Les piles',
      'Réglages du téléphone',
      'Appui long sur une carte',
      'Languette de droite',
      'Appui long sur une languette',
      'Bandeau « Annuler »',
      'Retour d’Android',
      'Défausse de fin de tour',
      'Verrou portrait',
      'Vibrations',
      'Installer l’application',
    ]) {
      expect(aide.textContent).toContain(texte)
    }
    for (const texte of ['E  Espace', 'Alt + glisser', 'Double-clic']) expect(aide.textContent).not.toContain(texte)
  })

  it('chaque ligne du téléphone a sa traduction anglaise', () => {
    render(<VoletAideAuto ouvert ouvrir={rien} fermer={rien} telephone />)
    const aide = screen.getByRole('dialog', { name: 'Aide' })
    const textes = [...aide.querySelectorAll('h3, kbd, dd')].map((n) => n.textContent ?? '')
    const manquants = textes.filter((texte) => !DICO_EN_BASE[texte])
    expect(manquants).toEqual([])
  })

  it('sur PC et sur téléphone : le groupe « Cartes empilées » explique les piles (State of Flow, cartes glissées)', () => {
    for (const telephone of [false, true]) {
      const { unmount } = render(<VoletAideAuto ouvert ouvrir={rien} fermer={rien} telephone={telephone} />)
      const aide = screen.getByRole('dialog', { name: 'Aide' })
      for (const texte of [
        'Cartes empilées',
        'Contour en pointillés dorés',
        'State of Flow',
        'Pastille « Pile de cartes : N »',
        'Événement dans une pile',
        'pas resté en jeu par erreur',
      ]) {
        expect(aide.textContent).toContain(texte)
      }
      unmount()
    }
  })

  it('le groupe « Cartes empilées » a sa traduction anglaise, sur PC comme sur téléphone', () => {
    for (const telephone of [false, true]) {
      const { container, unmount } = render(<VoletAideAuto ouvert ouvrir={rien} fermer={rien} telephone={telephone} />)
      const groupe = [...container.querySelectorAll('section.aide-manuel-groupe')].find((g) => g.querySelector('h3')?.textContent === 'Cartes empilées')
      expect(groupe).toBeDefined()
      const textes = [...(groupe as Element).querySelectorAll('h3, kbd, dd')].map((n) => n.textContent ?? '')
      expect(textes.length).toBeGreaterThanOrEqual(7)
      expect(textes.filter((texte) => !DICO_EN_BASE[texte])).toEqual([])
      unmount()
    }
  })
})
