// Le voile sur la table pendant qu'une etape est a l'ecran.
//
// Imperatif, comme halo-statut.ts et pas-a-pas.ts : on pose une classe sur le
// body, on la retire ensuite. Passer par React ferait re-rendre le plateau
// entier a chaque etape, pour une decoration transitoire.
//
// La scene centrale (DeroulePhase) porte les cartes elle-meme : ce hook ne
// touche plus a aucune carte de la table.
import { afterEach, describe, expect, it } from 'vitest'
import { renderHook } from '@testing-library/react'
import { useDerouleScene } from './useDerouleScene'
import type { EtapeDeroule } from './deroule-phase'

const etape = (extra: Partial<EtapeDeroule> = {}): EtapeDeroule => ({
  cle: 'k',
  temps: 'sbires',
  titre: 'attaque',
  regle: 'regle:activations',
  boosts: [],
  ...extra,
})

const voile = () => document.body.classList.contains('deroule-voile')

afterEach(() => {
  document.body.className = ''
  document.body.innerHTML = ''
})

describe('le voile de la scene', () => {
  it('assombrit la table pour une etape qui montre des cartes', () => {
    renderHook(() => useDerouleScene(etape({ carteId: 50 }), true))
    expect(voile()).toBe(true)
  })

  it('assombrit aussi sans que la carte soit sur la table', () => {
    // La scene tire ses cartes de l'index du monde, pas du DOM : une carte
    // partie a la defausse (un boost) se montre quand meme.
    renderHook(() => useDerouleScene(etape({ carteId: 999 }), true))
    expect(voile()).toBe(true)
  })

  it('n assombrit rien sur le bilan', () => {
    renderHook(() => useDerouleScene(etape({ temps: 'bilan', titre: 'bilan', bilan: [] }), true))
    expect(voile()).toBe(false)
  })

  it('n assombrit rien quand la scene est coupee', () => {
    renderHook(() => useDerouleScene(etape({ carteId: 50 }), false))
    expect(voile()).toBe(false)
  })

  it('retire le voile au demontage', () => {
    const { unmount } = renderHook(() => useDerouleScene(etape({ carteId: 50 }), true))
    expect(voile()).toBe(true)
    unmount()
    expect(voile()).toBe(false)
  })

  it('retire le voile quand l etape suivante n a rien a montrer', () => {
    const { rerender } = renderHook(({ e }) => useDerouleScene(e, true), {
      initialProps: { e: etape({ carteId: 50 }) },
    })
    expect(voile()).toBe(true)
    rerender({ e: etape({ cle: 'bilan', temps: 'bilan', titre: 'bilan', bilan: [] }) })
    expect(voile()).toBe(false)
  })

  it('ne pose pas de carte en avant sur la table', () => {
    const scene = document.createElement('div')
    scene.className = 'plateau-scene'
    const carte = document.createElement('article')
    carte.className = 'scan-card'
    carte.setAttribute('data-card-id', '50')
    scene.append(carte)
    document.body.append(scene)
    renderHook(() => useDerouleScene(etape({ carteId: 50, cibleId: 12 }), true))
    expect(carte.className).toBe('scan-card')
  })
})
