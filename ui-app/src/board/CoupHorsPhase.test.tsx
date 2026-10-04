// Decision du 03/10/2026 : hors phase du mechant (tour d'un joueur), une
// attaque ou une manigance du mechant ouvre le cartouche pour ce seul coup.
import { afterEach, describe, expect, it } from 'vitest'
import { fireEvent, render } from '@testing-library/react'
import { CoupHorsPhase } from './CoupHorsPhase'
import type { EtapeDeroule } from './deroule-phase'
import { ecran as screen } from '../test-textes'

afterEach(() => window.localStorage.clear())

const coup = (cle: string, extra: Partial<EtapeDeroule> = {}): EtapeDeroule => ({
  cle, temps: 'mechant', titre: 'attaque', etat: 'resolu', regle: '', horsPhase: true,
  auteurNom: 'Ultron', cibleNom: 'Shuri', montant: 5, boosts: [], ...extra,
})

describe('le cartouche d un coup hors phase', () => {
  it('montre le coup, puis se ferme sur Continuer', () => {
    const { container } = render(<CoupHorsPhase etapes={[coup('a')]} />)
    expect(screen.getByText('Hors de la phase du méchant')).toBeInTheDocument()
    expect(screen.getByText('Ultron attaque Shuri')).toBeInTheDocument()
    expect(screen.getByText('→ 5 dégâts')).toBeInTheDocument()
    fireEvent.click(screen.getByRole('button', { name: 'Continuer' }))
    expect(container).toBeEmptyDOMElement()
  })

  it('ne remontre pas un coup deja vu, mais montre le suivant', () => {
    const { container, rerender } = render(<CoupHorsPhase etapes={[coup('a')]} />)
    fireEvent.click(screen.getByRole('button', { name: 'Continuer' }))
    rerender(<CoupHorsPhase etapes={[coup('a')]} />)
    expect(container).toBeEmptyDOMElement()
    rerender(<CoupHorsPhase etapes={[coup('a'), coup('b', { cibleNom: 'Okoye' })]} />)
    expect(screen.getByText('Ultron attaque Okoye')).toBeInTheDocument()
  })

  it('attend la resolution : rien sur une simple annonce', () => {
    const { container } = render(<CoupHorsPhase etapes={[coup('a', { etat: 'annonce', montant: undefined })]} />)
    expect(container).toBeEmptyDOMElement()
  })

  it('ne montre pas les coups deja la au premier rendu (rechargement de page)', () => {
    const { container } = render(<CoupHorsPhase etapes={[coup('a')]} ignorerLesPremiers />)
    expect(container).toBeEmptyDOMElement()
  })
})
