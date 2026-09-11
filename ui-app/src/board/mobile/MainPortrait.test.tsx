import { fireEvent, render, screen } from '@testing-library/react'
import { describe, expect, it, vi } from 'vitest'
import { MainPortrait } from './MainPortrait'
import type { UniteAffichee } from '../zones'

const unite = (nom: string): UniteAffichee =>
  ({ cle: nom, carte: { id: nom, name: nom, kind: 'event', imageUrl: '/s' }, attachees: [] }) as unknown as UniteAffichee

describe('MainPortrait', () => {
  it('rend une rangee qui defile, une carte par unite', () => {
    const { container } = render(
      <MainPortrait unites={[unite('Quinjet'), unite('Backflip')]} onOuvrir={() => {}} />
    )
    expect(container.querySelectorAll('.main-portrait .scan-card')).toHaveLength(2)
    expect(container.querySelector('.main-portrait')).toHaveClass('defile')
  })

  it('dit combien de cartes on a en main', () => {
    render(<MainPortrait unites={[unite('a'), unite('b'), unite('c')]} onOuvrir={() => {}} />)
    expect(screen.getByText('3')).toBeInTheDocument()
    expect(screen.getByText('en main')).toBeInTheDocument()
  })

  it('un tap ouvre la carte', () => {
    const onOuvrir = vi.fn()
    const { container } = render(<MainPortrait unites={[unite('Quinjet')]} onOuvrir={onOuvrir} />)
    fireEvent.click(container.querySelector('.main-portrait .scan-card') as Element)
    expect(onOuvrir).toHaveBeenCalledTimes(1)
  })

  it('main vide : on le dit au lieu de laisser un trou', () => {
    render(<MainPortrait unites={[]} onOuvrir={() => {}} />)
    expect(screen.getByText('Ta main est vide')).toBeInTheDocument()
  })
})
