import { fireEvent, render, screen } from '@testing-library/react'
import { describe, expect, it, vi } from 'vitest'
import { BandeauPortrait } from './BandeauPortrait'
import type { World } from '../world'

const monde = (phase: string, round = 2): World =>
  ({ render_id: 1, round_id: round, phase, players: [{ area_hero: [{ name: '* Steve Rogers' }] }] }) as unknown as World

describe('BandeauPortrait', () => {
  it('dit le round, la phase et a qui de jouer', () => {
    render(<BandeauPortrait monde={monde('Player 1 Turn')} quiAgit="À toi de jouer" />)
    expect(screen.getByText('Round 2')).toBeInTheDocument()
    expect(screen.getByText('Tour de Steve Rogers')).toBeInTheDocument()
    expect(screen.getByText('À toi de jouer')).toBeInTheDocument()
  })

  it('dit qui on attend quand ce n est pas notre tour', () => {
    render(<BandeauPortrait monde={monde('Enemy Activation')} quiAgit="Le méchant agit" />)
    expect(screen.getByText('Le méchant agit')).toBeInTheDocument()
  })

  it('sans menu ni action, rien de plus que l etat', () => {
    render(<BandeauPortrait monde={monde('Player 1 Turn')} />)
    expect(document.querySelector('.portrait-menu-bouton')).toBeNull()
    expect(document.querySelector('.portrait-action')).toBeNull()
  })

  it('le bouton « … » ouvre le menu en feuille, le voile le referme', () => {
    render(<BandeauPortrait monde={monde('Player 1 Turn')} menu={<button type="button" className="bh-bouton bh-options">Options</button>} />)
    expect(document.querySelector('.portrait-menu')).toBeNull()
    fireEvent.click(document.querySelector('.portrait-menu-bouton')!)
    expect(document.querySelector('.portrait-menu .bh-options')).toBeInTheDocument()
    expect(document.querySelector('.portrait-menu-bouton')).toHaveAttribute('aria-expanded', 'true')
    fireEvent.pointerDown(document.querySelector('.portrait-menu-voile')!)
    expect(document.querySelector('.portrait-menu')).toBeNull()
  })

  it("la feuille du menu est rendue dans document.body : sous le panneau de phase (z 540), elle serait cachée", () => {
    render(<BandeauPortrait monde={monde('Player 1 Turn')} menu={<button type="button" className="bh-bouton bh-options">Options</button>} />)
    fireEvent.click(document.querySelector('.portrait-menu-bouton')!)
    const feuille = document.querySelector('.portrait-menu')!
    expect(feuille.parentElement).toBe(document.body)
    expect(document.querySelector('.portrait-bandeau')!.contains(feuille)).toBe(false)
  })

  it('le bouton d action principal porte son libelle, sa suggestion, et agit', () => {
    const agir = vi.fn()
    render(<BandeauPortrait monde={monde('Player 1 Turn')} actionPrincipale={{ libelle: 'Fin du tour', suggere: true, agir }} />)
    const bouton = document.querySelector('.portrait-action')!
    expect(bouton).toHaveTextContent('Fin du tour ✓')
    expect(bouton).toHaveClass('est-suggere')
    fireEvent.click(bouton)
    expect(agir).toHaveBeenCalledTimes(1)
  })
})
