// « Revoir la phase du méchant » dans le volet du journal (03/10/2026).
import { afterEach, describe, expect, it } from 'vitest'
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
})
