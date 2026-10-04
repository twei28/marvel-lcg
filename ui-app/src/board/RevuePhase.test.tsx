// « Revoir la phase du méchant » (decision du 03/10/2026) : apres la phase, en
// lecture seule, depuis le volet du journal. La frise des six onglets, un clic
// sur un onglet liste ses coups, un clic sur un coup en donne le detail.
import { afterEach, describe, expect, it } from 'vitest'
import { fireEvent, render } from '@testing-library/react'
import { RevuePhase } from './RevuePhase'
import type { EtapeDeroule } from './deroule-phase'
import { ecran as screen } from '../test-textes'

afterEach(() => window.localStorage.clear())

const phase: EtapeDeroule[] = [
  { cle: 'm', temps: 'menace', titre: 'menace', regle: '', cibleNom: 'Effraction', montant: 1, boosts: [] },
  { cle: 'v', temps: 'mechant', titre: 'attaque', etat: 'resolu', regle: '', auteurNom: 'Rhino', cibleNom: 'Shuri', montant: 3, base: 3, defense: 0, boosts: [] },
  { cle: 's1', temps: 'sbires', titre: 'attaque', etat: 'resolu', regle: '', auteurNom: 'Drone', cibleNom: 'Shuri', montant: 1, base: 1, defense: 0, boosts: [] },
  { cle: 's2', temps: 'sbires', titre: 'attaque', etat: 'resolu', regle: '', auteurNom: 'Hydra', cibleNom: 'Shuri', montant: 2, base: 2, defense: 0, boosts: [] },
]

describe('la revue de la phase du mechant', () => {
  it('montre les six onglets, tous passes, chacun avec son resultat', () => {
    render(<RevuePhase etapes={phase} />)
    const onglets = document.querySelectorAll('.deroule-temps li')
    expect(onglets).toHaveLength(6)
    expect(onglets[1].textContent).toContain('3 dégâts')
    expect(onglets[2].textContent).toContain('3 dégâts')
    // Le Bilan s'ouvre d'abord : ce que la phase a coute.
    expect(screen.getByText('Shuri a pris 6 dégâts')).toBeInTheDocument()
  })

  it('un onglet liste ses coups, un coup donne son detail, sans aucun bouton Suivant', () => {
    render(<RevuePhase etapes={phase} />)
    fireEvent.click(document.querySelectorAll('.deroule-temps li button')[2])
    const lignes = document.querySelectorAll('.deroule-relecture-liste button')
    expect(lignes).toHaveLength(2)
    fireEvent.click(lignes[0])
    expect(screen.getByText('Drone attaque Shuri')).toBeInTheDocument()
    expect(screen.getByText('→ 1 dégât')).toBeInTheDocument()
    expect(screen.queryByRole('button', { name: /Suivant/ })).toBeNull()
  })

  it('dit les temps vides', () => {
    render(<RevuePhase etapes={phase} />)
    fireEvent.click(document.querySelectorAll('.deroule-temps li button')[4])
    expect(screen.getByText('Rien à révéler')).toBeInTheDocument()
  })
  it('nomme les cartes en francais quand le plateau les connait', () => {
    const avecIds = phase.map((e) => (e.cle === 'm' ? { ...e, cibleId: 9, cibleNom: 'The Break-In!' } : e))
    render(<RevuePhase etapes={avecIds} nomFr={(id) => (id === 9 ? 'L’Effraction !' : undefined)} />)
    expect(screen.getByText('L’Effraction ! a gagné 1 menace')).toBeInTheDocument()
  })
})
