import { fireEvent, render, screen } from '@testing-library/react'
import { afterEach, describe, expect, it, vi } from 'vitest'
import { MainPortrait } from './MainPortrait'
import { APPUI_LONG_MS } from './useAppuiLong'
import type { UniteAffichee } from '../zones'

const unite = (nom: string): UniteAffichee =>
  ({ cle: nom, carte: { id: nom, name: nom, kind: 'event', imageUrl: '/s' }, attachees: [] }) as unknown as UniteAffichee

describe('MainPortrait', () => {
  it('fermee, elle ne rend rien : la main vit derriere son encoche', () => {
    const { container } = render(<MainPortrait ouverte={false} onFermer={() => {}} unites={[unite('a')]} onOuvrir={() => {}} />)
    expect(container.querySelector('.main-feuille')).toBeNull()
  })

  it('ouverte, un tap sur le voile ou sur Fermer la referme', () => {
    const onFermer = vi.fn()
    render(<MainPortrait ouverte onFermer={onFermer} unites={[unite('a')]} onOuvrir={() => {}} />)
    expect(document.querySelector('.main-feuille')).toHaveAttribute('role', 'dialog')
    fireEvent.pointerDown(document.querySelector('.main-feuille-voile')!)
    fireEvent.click(document.querySelector('.main-feuille-fermer')!)
    expect(onFermer).toHaveBeenCalledTimes(2)
  })

  it('rend une rangee qui defile, une carte par unite', () => {
    const { container } = render(
      <MainPortrait ouverte onFermer={() => {}} unites={[unite('Quinjet'), unite('Backflip')]} onOuvrir={() => {}} />
    )
    expect(container.querySelectorAll('.main-portrait .scan-card')).toHaveLength(2)
    expect(container.querySelector('.main-portrait')).toHaveClass('defile')
  })

  it('dit combien de cartes on a en main', () => {
    render(<MainPortrait ouverte onFermer={() => {}} unites={[unite('a'), unite('b'), unite('c')]} onOuvrir={() => {}} />)
    expect(screen.getByText('3')).toBeInTheDocument()
    expect(screen.getByText('en main')).toBeInTheDocument()
  })

  it('un tap ouvre la carte', () => {
    const onOuvrir = vi.fn()
    const { container } = render(<MainPortrait ouverte onFermer={() => {}} unites={[unite('Quinjet')]} onOuvrir={onOuvrir} />)
    fireEvent.click(container.querySelector('.main-portrait .scan-card') as Element)
    expect(onOuvrir).toHaveBeenCalledTimes(1)
  })

  it('une carte CIBLE (défausse de fin de tour) se coche d’un tap, sans ouvrir sa fiche', () => {
    const onOuvrir = vi.fn()
    const cocher = vi.fn()
    const cible = { ...unite('Quinjet'), carte: { ...unite('Quinjet').carte, state: 'targetable', onSelect: cocher } } as UniteAffichee
    const cochee = { ...unite('Backflip'), carte: { ...unite('Backflip').carte, state: 'selected', onSelect: cocher } } as UniteAffichee
    const { container } = render(<MainPortrait ouverte onFermer={() => {}} unites={[cible, cochee]} onOuvrir={onOuvrir} />)
    const cartes = container.querySelectorAll('.main-portrait .scan-card')
    fireEvent.click(cartes[0] as Element)
    fireEvent.click(cartes[1] as Element)
    expect(cocher).toHaveBeenCalledTimes(2)
    expect(onOuvrir).not.toHaveBeenCalled()
  })

  it('une carte JOUABLE (non cible) ouvre toujours sa fiche au tap', () => {
    const onOuvrir = vi.fn()
    const jouer = vi.fn()
    const jouable = { ...unite('Quinjet'), carte: { ...unite('Quinjet').carte, state: 'playable', onSelect: jouer } } as UniteAffichee
    const { container } = render(<MainPortrait ouverte onFermer={() => {}} unites={[jouable]} onOuvrir={onOuvrir} />)
    fireEvent.click(container.querySelector('.main-portrait .scan-card') as Element)
    expect(onOuvrir).toHaveBeenCalledTimes(1)
    expect(jouer).not.toHaveBeenCalled()
  })

  it('main vide : on le dit au lieu de laisser un trou', () => {
    render(<MainPortrait ouverte onFermer={() => {}} unites={[]} onOuvrir={() => {}} />)
    expect(screen.getByText('Ta main est vide')).toBeInTheDocument()
  })

  describe('zone 3 : toucher puis « Jouer », toucher long pour lire', () => {
    afterEach(() => {
      vi.useRealTimers()
    })

    const jouableQuinjet = () =>
      ({ ...unite('Quinjet'), carte: { ...unite('Quinjet').carte, state: 'playable', onSelect: vi.fn() } }) as UniteAffichee

    it('toucher une carte jouable la choisit, « Jouer » la joue, sans ouvrir sa fiche', () => {
      const onOuvrir = vi.fn()
      const onJouer = vi.fn()
      const carte = jouableQuinjet()
      const { container } = render(
        <MainPortrait ouverte onFermer={() => {}} unites={[carte]} onOuvrir={onOuvrir} onJouer={onJouer} jouable={() => true} />
      )
      expect(container.querySelector('.main-feuille-jouer')).toBeNull()
      fireEvent.click(container.querySelector('.main-portrait .scan-card') as Element)
      expect(container.querySelector('.main-portrait-carte')).toHaveClass('est-choisie')
      expect(onOuvrir).not.toHaveBeenCalled()
      fireEvent.click(screen.getByRole('button', { name: 'Jouer' }))
      expect(onJouer).toHaveBeenCalledTimes(1)
      expect(onJouer.mock.calls[0]?.[0]).toMatchObject({ cle: 'Quinjet' })
      // Jouee : le choix retombe, le bouton disparait.
      expect(container.querySelector('.main-feuille-jouer')).toBeNull()
    })

    it('un second toucher sur la carte choisie la repose ; « Lire » l ouvre en grand', () => {
      const onOuvrir = vi.fn()
      const { container } = render(
        <MainPortrait ouverte onFermer={() => {}} unites={[jouableQuinjet()]} onOuvrir={onOuvrir} onJouer={() => {}} jouable={() => true} />
      )
      const scan = container.querySelector('.main-portrait .scan-card') as Element
      fireEvent.click(scan)
      fireEvent.click(screen.getByRole('button', { name: 'Lire' }))
      expect(onOuvrir).toHaveBeenCalledTimes(1)
      fireEvent.click(scan)
      expect(container.querySelector('.main-portrait-carte')).not.toHaveClass('est-choisie')
      expect(container.querySelector('.main-feuille-jouer')).toBeNull()
    })

    it('une carte qui n est plus jouable perd son bouton « Jouer »', () => {
      let peutJouer = true
      const carte = jouableQuinjet()
      const { container, rerender } = render(
        <MainPortrait ouverte onFermer={() => {}} unites={[carte]} onOuvrir={() => {}} onJouer={() => {}} jouable={() => peutJouer} />
      )
      fireEvent.click(container.querySelector('.main-portrait .scan-card') as Element)
      expect(container.querySelector('.main-feuille-jouer')).not.toBeNull()
      peutJouer = false
      rerender(
        <MainPortrait ouverte onFermer={() => {}} unites={[carte]} onOuvrir={() => {}} onJouer={() => {}} jouable={() => peutJouer} />
      )
      expect(container.querySelector('.main-feuille-jouer')).toBeNull()
    })

    it('le toucher long LIT la carte, il ne la joue plus', () => {
      vi.useFakeTimers()
      const onOuvrir = vi.fn()
      const onJouer = vi.fn()
      const { container } = render(
        <MainPortrait ouverte onFermer={() => {}} unites={[jouableQuinjet()]} onOuvrir={onOuvrir} onJouer={onJouer} jouable={() => true} />
      )
      const porteuse = container.querySelector('.main-portrait-carte') as Element
      fireEvent.pointerDown(porteuse)
      vi.advanceTimersByTime(APPUI_LONG_MS)
      expect(onOuvrir).toHaveBeenCalledTimes(1)
      expect(onJouer).not.toHaveBeenCalled()
    })

    it('le clic qui suit le toucher long ne choisit pas la carte en plus', () => {
      vi.useFakeTimers()
      const onOuvrir = vi.fn()
      const { container } = render(
        <MainPortrait ouverte onFermer={() => {}} unites={[jouableQuinjet()]} onOuvrir={onOuvrir} onJouer={() => {}} jouable={() => true} />
      )
      const porteuse = container.querySelector('.main-portrait-carte') as Element
      fireEvent.pointerDown(porteuse)
      vi.advanceTimersByTime(APPUI_LONG_MS)
      fireEvent.pointerUp(porteuse)
      fireEvent.click(container.querySelector('.main-portrait .scan-card') as Element)
      expect(onOuvrir).toHaveBeenCalledTimes(1)
      expect(container.querySelector('.main-portrait-carte')).not.toHaveClass('est-choisie')
    })

    it('un toucher court sur une carte non jouable l ouvre normalement', () => {
      vi.useFakeTimers()
      const onOuvrir = vi.fn()
      const onJouer = vi.fn()
      const { container } = render(
        <MainPortrait ouverte onFermer={() => {}} unites={[unite('Quinjet')]} onOuvrir={onOuvrir} onJouer={onJouer} jouable={() => false} />
      )
      const porteuse = container.querySelector('.main-portrait-carte') as Element
      fireEvent.pointerDown(porteuse)
      fireEvent.pointerUp(porteuse)
      fireEvent.click(container.querySelector('.main-portrait .scan-card') as Element)
      expect(onOuvrir).toHaveBeenCalledTimes(1)
      expect(onJouer).not.toHaveBeenCalled()
    })
  })
})
