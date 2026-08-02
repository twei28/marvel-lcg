import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { renderHook } from '@testing-library/react'
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

describe('useModeMobile', () => {
  const ecouteurs = new Set<(evenement: MediaQueryListEvent) => void>()
  let retraits = 0

  beforeEach(() => {
    ecouteurs.clear()
    retraits = 0
    window.localStorage.clear()
    // Bouchon pilotable : celui de test-setup.ts repond toujours matches: false.
    vi.stubGlobal('matchMedia', (media: string) => ({
      media,
      matches: true,
      addEventListener: (_: string, ecouteur: (evenement: MediaQueryListEvent) => void) => {
        ecouteurs.add(ecouteur)
      },
      removeEventListener: () => {
        retraits += 1
      },
    }))
  })

  afterEach(() => {
    vi.unstubAllGlobals()
  })

  it('rend le mode mobile quand la media query correspond', () => {
    const { result } = renderHook(() => useModeMobile())
    expect(result.current.mode).toBe('mobile')
  })

  it('laisse le reglage force gagner sur la media query', () => {
    ecrireReglage('pc')
    const { result } = renderHook(() => useModeMobile())
    expect(result.current.mode).toBe('pc')
  })

  it('retire son ecouteur au demontage', () => {
    const { unmount } = renderHook(() => useModeMobile())
    expect(ecouteurs.size).toBe(1)
    unmount()
    expect(retraits).toBe(1)
  })
})
