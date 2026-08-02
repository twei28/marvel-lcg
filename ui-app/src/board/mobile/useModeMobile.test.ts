import { beforeEach, describe, expect, it, vi } from 'vitest'
import { renderHook, act } from '@testing-library/react'
import { CLE_MODE, ecrireReglage, lireReglage, modeEffectif, useModeMobile } from './useModeMobile'

describe('modeEffectif', () => {
  it('suit la media query en mode auto', () => {
    expect(modeEffectif('auto', true)).toBe('mobile')
    expect(modeEffectif('auto', false)).toBe('pc')
  })

  it('ignore la media query quand un mode est force', () => {
    expect(modeEffectif('mobile', false)).toBe('mobile')
    expect(modeEffectif('pc', true)).toBe('pc')
  })
})

describe('reglage memorise', () => {
  beforeEach(() => window.localStorage.clear())

  it('vaut auto quand rien n\'est memorise', () => {
    expect(lireReglage()).toBe('auto')
  })

  it('relit ce qui a ete ecrit', () => {
    ecrireReglage('mobile')
    expect(window.localStorage.getItem(CLE_MODE)).toBe('mobile')
    expect(lireReglage()).toBe('mobile')
  })

  it('retombe sur auto devant une valeur inconnue', () => {
    window.localStorage.setItem(CLE_MODE, 'tablette')
    expect(lireReglage()).toBe('auto')
  })
})

describe('useModeMobile hook', () => {
  beforeEach(() => window.localStorage.clear())

  it('retourne mode, reglage et changer', () => {
    const { result } = renderHook(() => useModeMobile())
    expect(result.current).toHaveProperty('mode')
    expect(result.current).toHaveProperty('reglage')
    expect(result.current).toHaveProperty('changer')
  })

  it('initialise le reglage depuis localStorage', () => {
    ecrireReglage('mobile')
    const { result } = renderHook(() => useModeMobile())
    expect(result.current.reglage).toBe('mobile')
  })

  it('change le reglage et le memorise', () => {
    const { result } = renderHook(() => useModeMobile())
    act(() => {
      result.current.changer('pc')
    })
    expect(result.current.reglage).toBe('pc')
    expect(lireReglage()).toBe('pc')
  })
})
