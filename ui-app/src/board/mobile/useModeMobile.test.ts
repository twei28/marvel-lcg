import { beforeEach, describe, expect, it } from 'vitest'
import { CLE_MODE, ecrireReglage, lireReglage, modeEffectif } from './useModeMobile'

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
