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

  describe('appui long : jouer sans passer par le tap', () => {
    afterEach(() => {
      vi.useRealTimers()
    })

    it('un appui long sur la carte appelle onJouer', () => {
      vi.useFakeTimers()
      const onJouer = vi.fn()
      const { container } = render(
        <MainPortrait ouverte onFermer={() => {}} unites={[unite('Quinjet')]} onOuvrir={() => {}} onJouer={onJouer} />
      )
      const porteuse = container.querySelector('.main-portrait-carte') as Element
      fireEvent.pointerDown(porteuse)
      vi.advanceTimersByTime(APPUI_LONG_MS)
      expect(onJouer).toHaveBeenCalledTimes(1)
      expect(onJouer.mock.calls[0]?.[0]).toMatchObject({ cle: 'Quinjet' })
    })

    it('sans onJouer, le maintien ne declenche rien (la main reste juste lisible)', () => {
      vi.useFakeTimers()
      const { container } = render(<MainPortrait ouverte onFermer={() => {}} unites={[unite('Quinjet')]} onOuvrir={() => {}} />)
      const porteuse = container.querySelector('.main-portrait-carte') as Element
      expect(() => {
        fireEvent.pointerDown(porteuse)
        vi.advanceTimersByTime(APPUI_LONG_MS)
      }).not.toThrow()
    })

    it('l appui long annule le tap qui suit : pas d ouverture apres avoir joue', () => {
      // Point de vigilance du brief : useAppuiLong ne supprime pas lui-meme le
      // clic qui suit le relachement du doigt, il expose seulement
      // `vientDeDeclencher()`. Sans le consulter au tap, on jouerait ET on
      // ouvrirait la carte pour un seul geste.
      vi.useFakeTimers()
      const onOuvrir = vi.fn()
      const onJouer = vi.fn()
      const { container } = render(
        <MainPortrait ouverte onFermer={() => {}} unites={[unite('Quinjet')]} onOuvrir={onOuvrir} onJouer={onJouer} />
      )
      const porteuse = container.querySelector('.main-portrait-carte') as Element
      fireEvent.pointerDown(porteuse)
      vi.advanceTimersByTime(APPUI_LONG_MS)
      fireEvent.pointerUp(porteuse)
      fireEvent.click(container.querySelector('.main-portrait .scan-card') as Element)
      expect(onJouer).toHaveBeenCalledTimes(1)
      expect(onOuvrir).not.toHaveBeenCalled()
    })

    it('un tap simple (sans maintien) ouvre toujours la carte normalement', () => {
      vi.useFakeTimers()
      const onOuvrir = vi.fn()
      const onJouer = vi.fn()
      const { container } = render(
        <MainPortrait ouverte onFermer={() => {}} unites={[unite('Quinjet')]} onOuvrir={onOuvrir} onJouer={onJouer} />
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
