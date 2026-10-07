// triche.test.ts — la bascule de pause manuelle (tâche 3).
//
// Le reste de triche.ts (soigner, blesser, deplacerVers...) est déjà couvert
// indirectement par CoucheTriche.test.tsx, qui monte le menu complet.
// `basculerPause` vise une route DISTINCTE (`/manuel_pause`, pas
// `/sandbox_command`) : ce fichier l'isole plutôt que d'ajouter un second
// style d'assertion au milieu de CoucheTriche.test.tsx.
import { afterEach, describe, expect, it, vi } from 'vitest'
import { basculerPause } from './triche'

afterEach(() => {
  vi.unstubAllGlobals()
})

describe('basculerPause (POST /manuel_pause)', () => {
  it('pose la pause : envoie actif=true, aucun champ qui (resolu cote serveur)', async () => {
    vi.stubGlobal('fetch', vi.fn(async () => ({ ok: true }) as Response))
    const reussi = await basculerPause(true)
    expect(reussi).toBe(true)
    expect(fetch).toHaveBeenCalledWith('/manuel_pause', expect.objectContaining({
      method: 'POST',
      body: JSON.stringify({ actif: true }),
    }))
  })

  it('reprend : envoie actif=false', async () => {
    vi.stubGlobal('fetch', vi.fn(async () => ({ ok: true }) as Response))
    await basculerPause(false)
    expect(fetch).toHaveBeenCalledWith('/manuel_pause', expect.objectContaining({
      body: JSON.stringify({ actif: false }),
    }))
  })

  it('rend faux si le moteur refuse', async () => {
    vi.stubGlobal('fetch', vi.fn(async () => ({ ok: false }) as Response))
    expect(await basculerPause(true)).toBe(false)
  })

  it('rend faux hors ligne, sans lever d\'exception', async () => {
    vi.stubGlobal('fetch', vi.fn(async () => { throw new Error('hors ligne') }))
    expect(await basculerPause(true)).toBe(false)
  })
})

describe('un geste accepté sonne comme en automatique (refonte des sons, 07/10/2026)', () => {
  it('le moteur accepte : le son de la famille du geste part', async () => {
    const sons = await import('./sons')
    const espion = vi.spyOn(sons, 'jouerGeste').mockImplementation(() => undefined)
    vi.stubGlobal('fetch', vi.fn(async () => ({ ok: true }) as Response))
    const { incliner } = await import('./triche')
    await incliner(12)
    expect(espion).toHaveBeenCalledWith(['Puzzle.Exhaust(12)'])
    espion.mockRestore()
  })

  it('le moteur refuse : aucun son', async () => {
    const sons = await import('./sons')
    const espion = vi.spyOn(sons, 'jouerGeste').mockImplementation(() => undefined)
    vi.stubGlobal('fetch', vi.fn(async () => ({ ok: false }) as Response))
    const { incliner } = await import('./triche')
    await incliner(12)
    expect(espion).not.toHaveBeenCalled()
    espion.mockRestore()
  })
})
