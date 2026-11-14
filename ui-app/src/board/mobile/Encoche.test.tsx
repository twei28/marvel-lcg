import { act, fireEvent, render } from '@testing-library/react'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { APPUI_LONG_DEPLACER_MS, Encoche, RATIO_MAX, RATIO_MIN, bornerRatio } from './Encoche'

// jsdom n'a pas PointerEvent : sans lui, clientX et clientY arrivent vides.
if (typeof window.PointerEvent === 'undefined') {
  class PointerEventDeTest extends MouseEvent {
    pointerId: number
    constructor(type: string, init: PointerEventInit = {}) {
      super(type, init)
      this.pointerId = init.pointerId ?? 1
    }
  }
  Object.defineProperty(window, 'PointerEvent', { value: PointerEventDeTest, configurable: true })
}

const ecran = (hauteur: number) =>
  Object.defineProperty(window, 'innerHeight', { value: hauteur, configurable: true })

describe('bornerRatio', () => {
  it('ramene la place dans les bornes, et une valeur absurde a une place sure', () => {
    expect(bornerRatio(0)).toBe(RATIO_MIN)
    expect(bornerRatio(2)).toBe(RATIO_MAX)
    expect(bornerRatio(0.5)).toBe(0.5)
    expect(bornerRatio(Number.NaN)).toBeLessThan(RATIO_MAX)
  })
})

describe('Encoche deplacable (signalement Yarro #40)', () => {
  beforeEach(() => {
    vi.useFakeTimers()
    window.localStorage.clear()
    ecran(1000)
  })
  afterEach(() => {
    vi.useRealTimers()
  })

  const monter = (cote: 'gauche' | 'droite' = 'gauche') => {
    const onOuvrir = vi.fn()
    const rendu = render(<Encoche cote={cote} libelle="Piles" onOuvrir={onOuvrir} />)
    return { onOuvrir, bouton: rendu.container.querySelector('button') as HTMLButtonElement }
  }

  it('un tap simple ouvre toujours', () => {
    const { bouton, onOuvrir } = monter()
    fireEvent.pointerDown(bouton, { clientX: 5, clientY: 500 })
    fireEvent.pointerUp(bouton)
    fireEvent.click(bouton)
    expect(onOuvrir).toHaveBeenCalledTimes(1)
  })

  it('un swipe vers l interieur ouvre toujours', () => {
    const { bouton, onOuvrir } = monter()
    fireEvent.pointerDown(bouton, { clientX: 5, clientY: 500 })
    fireEvent.pointerMove(bouton, { clientX: 40, clientY: 500 })
    expect(onOuvrir).toHaveBeenCalledTimes(1)
  })

  it('appui long puis glisser : la languette suit le doigt, retient sa place et n ouvre pas', () => {
    const { bouton, onOuvrir } = monter()
    fireEvent.pointerDown(bouton, { clientX: 5, clientY: 500 })
    act(() => {
      vi.advanceTimersByTime(APPUI_LONG_DEPLACER_MS + 10)
    })
    expect(bouton).toHaveClass('est-deplacee')
    fireEvent.pointerMove(bouton, { clientX: 5, clientY: 300 })
    expect(bouton.style.top).toBe('calc(30% - 36px)')
    fireEvent.pointerUp(bouton)
    fireEvent.click(bouton)
    expect(onOuvrir).not.toHaveBeenCalled()
    expect(bouton).not.toHaveClass('est-deplacee')
    expect(window.localStorage.getItem('marvel-encoche-gauche')).toBe('0.3')
  })

  it('glisser vers le haut deplace la languette tout de suite, sans appui long', () => {
    const { bouton, onOuvrir } = monter()
    fireEvent.pointerDown(bouton, { clientX: 5, clientY: 500 })
    fireEvent.pointerMove(bouton, { clientX: 6, clientY: 480 })
    expect(bouton).toHaveClass('est-deplacee')
    fireEvent.pointerMove(bouton, { clientX: 6, clientY: 400 })
    expect(bouton.style.top).toBe('calc(40% - 36px)')
    fireEvent.pointerUp(bouton)
    fireEvent.click(bouton)
    expect(onOuvrir).not.toHaveBeenCalled()
    expect(window.localStorage.getItem('marvel-encoche-gauche')).toBe('0.4')
  })

  it('ne sort jamais de l ecran', () => {
    const { bouton } = monter('droite')
    fireEvent.pointerDown(bouton, { clientX: 995, clientY: 500 })
    act(() => {
      vi.advanceTimersByTime(APPUI_LONG_DEPLACER_MS + 10)
    })
    fireEvent.pointerMove(bouton, { clientX: 995, clientY: -400 })
    expect(bouton.style.top).toBe(`calc(${RATIO_MIN * 100}% - 36px)`)
  })

  it('retrouve sa place au rechargement, chaque cote la sienne', () => {
    window.localStorage.setItem('marvel-encoche-gauche', '0.4')
    const { bouton } = monter('gauche')
    expect(bouton.style.top).toBe('calc(40% - 36px)')
    const { bouton: droite } = monter('droite')
    expect(droite.style.top).toBe('')
  })

  // Zone 3 (10/10/2026) : fine et semi-transparente au repos, pleine opacite
  // tant que le doigt la tient. La languette visible est `.encoche-corps`.
  it('s allume au toucher et s efface au relachement', () => {
    const { bouton } = monter()
    expect(bouton.querySelector('.encoche-corps')).not.toBeNull()
    expect(bouton).not.toHaveClass('est-touchee')
    fireEvent.pointerDown(bouton, { clientX: 5, clientY: 500 })
    expect(bouton).toHaveClass('est-touchee')
    fireEvent.pointerUp(bouton)
    expect(bouton).not.toHaveClass('est-touchee')
    fireEvent.pointerDown(bouton, { clientX: 5, clientY: 500 })
    fireEvent.pointerCancel(bouton)
    expect(bouton).not.toHaveClass('est-touchee')
  })

  // Temoin : un doigt qui part en travers AVANT la fin de l'appui long n'est
  // pas un maintien, la languette ne se saisit pas.
  it('ne se saisit pas si le doigt a bouge avant la fin de l appui long', () => {
    const { bouton } = monter()
    fireEvent.pointerDown(bouton, { clientX: 5, clientY: 500 })
    fireEvent.pointerMove(bouton, { clientX: 20, clientY: 500 })
    act(() => {
      vi.advanceTimersByTime(APPUI_LONG_DEPLACER_MS + 10)
    })
    expect(bouton).not.toHaveClass('est-deplacee')
  })
})
