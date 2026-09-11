import { render, screen } from '@testing-library/react'
import { describe, expect, it } from 'vitest'
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
})
