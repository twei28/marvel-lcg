import { afterEach, describe, expect, it, vi } from 'vitest'
import { sauverEnCours, sauverEnPartant } from './en-cours'

afterEach(() => vi.unstubAllGlobals())

describe('« Continuer la partie » : la sauvegarde au départ', () => {
  it('appelle /en_cours_sauver avec keepalive, pour survivre à la fermeture de la page', async () => {
    const fetchBouchon = vi.fn().mockResolvedValue({ ok: true })
    vi.stubGlobal('fetch', fetchBouchon)
    await sauverEnCours()
    expect(fetchBouchon).toHaveBeenCalledWith('/en_cours_sauver', expect.objectContaining({ keepalive: true }))
    sauverEnPartant()
    expect(fetchBouchon).toHaveBeenCalledTimes(2)
  })

  it('ne bloque jamais le départ : un moteur qui traîne laisse partir après le délai', async () => {
    vi.stubGlobal('fetch', vi.fn(() => new Promise(() => undefined)))
    const debut = Date.now()
    await sauverEnCours(60)
    expect(Date.now() - debut).toBeLessThan(500)
  })

  it('ne lève jamais, même si le réseau échoue', async () => {
    vi.stubGlobal('fetch', vi.fn().mockRejectedValue(new Error('hors ligne')))
    await expect(sauverEnCours()).resolves.toBeUndefined()
    expect(() => sauverEnPartant()).not.toThrow()
  })
})
