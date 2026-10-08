import { render, waitFor } from '@testing-library/react'
import { afterEach, describe, expect, it, vi } from 'vitest'
import { libelleDePartie, PageRelecture } from './PageRelecture'

afterEach(() => vi.unstubAllGlobals())

describe('mes dernieres parties (08/10/2026)', () => {
  it('le nom du fichier devient une date lisible et le scenario', () => {
    expect(libelleDePartie('partie-20261008-143005-Rhino.marvelreplay')).toBe('08/10/2026 14:30 · Rhino')
    expect(libelleDePartie('autre.marvelreplay')).toBe('autre.marvelreplay')
  })

  it('la liste s affiche quand la table en rend, avec Revoir et Telecharger', async () => {
    vi.stubGlobal(
      'fetch',
      vi.fn(async () => ({ ok: true, json: async () => [{ n: 0, nom: 'partie-20261008-143005-Rhino.marvelreplay' }] }))
    )
    const { container, getByText } = render(<PageRelecture />)
    await waitFor(() => expect(getByText('08/10/2026 14:30 · Rhino')).toBeInTheDocument())
    expect(container.querySelector('a[href="/get_ma_partie?n=0"]')).not.toBeNull()
  })

  it('rien quand la table ne rend aucune partie', async () => {
    vi.stubGlobal('fetch', vi.fn(async () => ({ ok: true, json: async () => [] })))
    const { container } = render(<PageRelecture />)
    await new Promise((r) => setTimeout(r, 10))
    expect(container.querySelector('.relecture-mes-parties')).toBeNull()
  })
})
