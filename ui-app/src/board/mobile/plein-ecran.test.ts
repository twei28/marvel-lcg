import { afterEach, describe, expect, it, vi } from 'vitest'
import { demanderPleinEcran, enPleinEcran, quitterPleinEcran } from './plein-ecran'

describe('le plein ecran au telephone', () => {
  afterEach(() => {
    vi.restoreAllMocks()
    Object.defineProperty(document, 'fullscreenElement', { value: null, configurable: true })
  })

  it('demande le plein ecran une fois, et avale le refus', async () => {
    const demande = vi.fn(() => Promise.reject(new Error('refuse')))
    Object.defineProperty(document.documentElement, 'requestFullscreen', { value: demande, configurable: true })
    expect(() => demanderPleinEcran()).not.toThrow()
    expect(demande).toHaveBeenCalledTimes(1)
    await Promise.resolve()
    // Deja en plein ecran : plus de demande.
    Object.defineProperty(document, 'fullscreenElement', { value: document.documentElement, configurable: true })
    demanderPleinEcran()
    expect(demande).toHaveBeenCalledTimes(1)
    expect(enPleinEcran()).toBe(true)
  })

  it('quitte le plein ecran seulement s il est actif', () => {
    const sortie = vi.fn(() => Promise.resolve())
    Object.defineProperty(document, 'exitFullscreen', { value: sortie, configurable: true })
    quitterPleinEcran()
    expect(sortie).not.toHaveBeenCalled()
    Object.defineProperty(document, 'fullscreenElement', { value: document.documentElement, configurable: true })
    quitterPleinEcran()
    expect(sortie).toHaveBeenCalledTimes(1)
  })

  it('ne fait rien sans API, sans lever', () => {
    Object.defineProperty(document.documentElement, 'requestFullscreen', { value: undefined, configurable: true })
    expect(() => demanderPleinEcran()).not.toThrow()
  })
})
