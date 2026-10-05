// « Revoir la phase du méchant » dans le volet du journal (03/10/2026).
import { afterEach, describe, expect, it, vi } from 'vitest'
import { fireEvent, render } from '@testing-library/react'
import { JournalConsole } from './JournalConsole'
import { ecran as screen } from '../test-textes'

afterEach(() => window.localStorage.clear())

const journal = (revuePhase?: React.ReactNode) => (
  <JournalConsole entrees={[]} effacer={() => {}} telechargerLog={() => {}} journalHeros={null} revuePhase={revuePhase} />
)

describe('le journal du volet', () => {
  it('offre de revoir la phase du mechant quand elle existe, puis d y revenir', () => {
    render(journal(<p>LA REVUE</p>))
    fireEvent.click(screen.getByRole('button', { name: 'Revoir la phase du méchant' }))
    expect(screen.getByText('LA REVUE')).toBeInTheDocument()
    fireEvent.click(screen.getByRole('button', { name: 'Retour au journal' }))
    expect(screen.queryByText('LA REVUE')).toBeNull()
  })

  it('ne propose rien sans phase a revoir', () => {
    render(journal())
    expect(screen.queryByRole('button', { name: 'Revoir la phase du méchant' })).toBeNull()
  })

  // Scene PC (D38, lot 5 de la refonte) : le bouton rouvre le cartouche du bas
  // en relecture ; le journal, lui, reste le journal.
  it('avec onRevoirPhase, le bouton appelle le rappel et ne bascule pas la vue', () => {
    const onRevoirPhase = vi.fn()
    render(
      <JournalConsole entrees={[]} effacer={() => {}} telechargerLog={() => {}} journalHeros={null} onRevoirPhase={onRevoirPhase} />
    )
    fireEvent.click(screen.getByRole('button', { name: 'Revoir la phase du méchant' }))
    expect(onRevoirPhase).toHaveBeenCalledTimes(1)
    expect(screen.queryByRole('button', { name: 'Retour au journal' })).toBeNull()
    expect(screen.getByText('Journal')).toBeInTheDocument()
  })
})
