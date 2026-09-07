import { afterEach, describe, expect, it, vi } from 'vitest'
import { renderHook } from '@testing-library/react'
import {
  demanderPleinEcranPaysage,
  doitDemanderPleinEcran,
  doitMontrerEcranPortrait,
  usePleinEcranAuPremierGeste,
} from './plein-ecran'

describe('regles pures', () => {
  it('demande le plein ecran seulement si le navigateur le supporte et qu\'on n\'y est pas', () => {
    expect(doitDemanderPleinEcran(false, true)).toBe(true)
    expect(doitDemanderPleinEcran(true, true)).toBe(false)
    expect(doitDemanderPleinEcran(false, false)).toBe(false)
  })

  it('montre l\'ecran portrait en portrait, et seulement la', () => {
    expect(doitMontrerEcranPortrait('portrait')).toBe(true)
    expect(doitMontrerEcranPortrait('paysage')).toBe(false)
  })
})

describe('demanderPleinEcranPaysage', () => {
  it('demande le plein ecran PUIS verrouille le paysage', async () => {
    const lock = vi.fn().mockResolvedValue(undefined)
    const requestFullscreen = vi.fn().mockResolvedValue(undefined)
    const doc = {
      fullscreenElement: null,
      documentElement: { requestFullscreen },
      defaultView: { screen: { orientation: { lock } } },
    } as unknown as Document
    await demanderPleinEcranPaysage(doc)
    expect(requestFullscreen).toHaveBeenCalledOnce()
    expect(lock).toHaveBeenCalledWith('landscape')
  })

  it('ne leve rien quand le plein ecran est refuse (le filet est l\'ecran portrait)', async () => {
    const doc = {
      fullscreenElement: null,
      documentElement: { requestFullscreen: vi.fn().mockRejectedValue(new Error('refus')) },
      defaultView: { screen: { orientation: { lock: vi.fn() } } },
    } as unknown as Document
    await expect(demanderPleinEcranPaysage(doc)).resolves.toBeUndefined()
  })

  it('ne leve rien sans API de plein ecran (iOS Safari)', async () => {
    const doc = { fullscreenElement: null, documentElement: {}, defaultView: { screen: {} } } as unknown as Document
    await expect(demanderPleinEcranPaysage(doc)).resolves.toBeUndefined()
  })
})

describe('usePleinEcranAuPremierGeste', () => {
  afterEach(() => vi.restoreAllMocks())

  it('demande le plein ecran au PREMIER pointerdown, et une seule fois', () => {
    const requestFullscreen = vi.fn().mockResolvedValue(undefined)
    document.documentElement.requestFullscreen = requestFullscreen
    renderHook(() => usePleinEcranAuPremierGeste(true))
    document.dispatchEvent(new Event('pointerdown'))
    document.dispatchEvent(new Event('pointerdown'))
    expect(requestFullscreen).toHaveBeenCalledOnce()
  })

  it('ne fait rien quand il est inactif', () => {
    const requestFullscreen = vi.fn().mockResolvedValue(undefined)
    document.documentElement.requestFullscreen = requestFullscreen
    renderHook(() => usePleinEcranAuPremierGeste(false))
    document.dispatchEvent(new Event('pointerdown'))
    expect(requestFullscreen).not.toHaveBeenCalled()
  })
})
